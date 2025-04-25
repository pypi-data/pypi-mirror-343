# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""Appliance Support For Pytorch."""
import functools
import itertools
import logging
import multiprocessing
import multiprocessing.dummy
import multiprocessing.pool
import os
import sys
import time
import uuid
from collections import defaultdict
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from contextlib import ExitStack, contextmanager
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from math import prod
from pathlib import Path
from threading import Event, Lock
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import dill
import grpc
import numpy as np
import torch
from tqdm import tqdm

import cerebras.pytorch as cstorch
from cerebras.appliance.appliance_client import ApplianceClient
from cerebras.appliance.appliance_manager import (
    ApplianceManager,
    TensorGrouper,
    TensorTransferTracker,
)
from cerebras.appliance.cluster.client import ClusterManagementClient
from cerebras.appliance.cluster.cluster_details import ClusterDetailsParser
from cerebras.appliance.cluster_config import ClusterConfig
from cerebras.appliance.data.conversions import rtfx_dtype_from_np_dtype
from cerebras.appliance.errors import (
    ApplianceClientException,
    ApplianceDropModeComplete,
    ApplianceResourceExhausted,
    ApplianceTensorDropped,
    register_grpc_error_pickler,
)
from cerebras.appliance.pb.framework.appliance_service_pb2 import (
    CompileRequest,
    CompileResponse,
    InitRequest,
    LoadRequest,
    RunInferenceRequest,
    RunRequest,
    SendCheckRequest,
    SendDeferredInputRequest,
    TokenizerInfo,
)
from cerebras.appliance.pb.workflow.appliance.common.common_config_pb2 import (
    ClusterDetails,
    DebugArgs,
    FrameworkType,
)
from cerebras.appliance.pb.workflow.appliance.common.message_queue_pb2 import (
    ValidTopics,
)
from cerebras.appliance.pb.ws.cross_compile_state_pb2 import CrossCompileState
from cerebras.appliance.storage.h5_storage import hdf5_locking
from cerebras.appliance.utils import limit_mp_threads, short_temp_dir
from cerebras.appliance.utils.signal import on_sigint
from cerebras.pytorch import cerebras_pytorch_lib
from cerebras.pytorch.backend import current_backend_impl
from cerebras.pytorch.core.appliance_utils import (
    assign_tensor_ids_to_shards,
    np_array_to_rtfx_proto,
    np_array_to_rtfx_scalar,
)
from cerebras.pytorch.saver.checkpoint_reader import CheckpointReader
from cerebras.pytorch.saver.pt_h5_saver import PyTorchH5Saver
from cerebras.pytorch.saver.storage import (
    DeferredTensor,
    lazy_tensor_data_wrapper,
)
from cerebras.pytorch.storage.utils import (
    torch_to_np_dtype,
    torch_to_rtfx_dtype,
)
from cerebras.pytorch.utils.nest import serialize_visit_fns


class ApplianceMode(ApplianceManager):
    """Manage pytorch interactions with the appliance."""

    # pylint: disable=signature-differs
    def __init__(
        self,
        artifact_dir: str,
        compile_dir: str,
        cluster_config: ClusterConfig,
        checkpoint_reader_cls=CheckpointReader,
        op_profiler_config: Optional[LoadRequest.OpProfilerConfig] = None,
    ):
        super().__init__(
            config=deepcopy(cluster_config),
            debug_args=deepcopy(cstorch.backends.csx.debug.debug_args),
            compile_dir=Path(compile_dir),
            artifact_dir=Path(artifact_dir),
            framework_type=FrameworkType.PYTORCH,
            op_profiler_config=op_profiler_config,
        )

        self._last_fetched_iteration = 0
        self.output_names = []
        self.weight_names = {}
        self._output_name_to_idx = {}
        self.auxilliary_state_names = {}
        self._async_grpc_client = None

        # Overwrite the number of transfer threads to be used for data transfer
        # using the global configuration flag
        self._transfer_threads = (
            cstorch.backends.csx.performance.transfer_processes
        )
        # Add fabric type blacklist to the management client arguments
        self._mgmt_client_args["fabric_type_blacklist"] = (
            cstorch.backends.csx.debug.fabric_type_blacklist
        )

        self.checkpoint_reader_cls = checkpoint_reader_cls
        self.tracker_execute = current_backend_impl().appliance_tracker

        # A set of rt tensor names that are sparsity masks.
        self._sparsity_mask_names = set()

        # Counter to track the initial checkpoint id.
        self._initial_ckpt_id = 0

        self._exec_prep_is_done = False

        self.is_sidecar_available = False

        self._transferred_weights = set()
        self._sent_weights = set()

    def receive_activations(self, iteration: int):
        """Get activations from appliance.

        Args:
            iteration: Iteration to receive activations for. Note that
                activations are received sequentially. So, if this number is
                a few steps ahead of the last iteration that was received, then
                it counts from last fetched iteration up to this iteration, but
                only returns activations for the requested iteration.
        """
        for i in range(iteration, iteration + 1):
            activations = super().receive_activations(i)

            activation_map = dict()
            received_activations = dict()
            for name, tensor in activations.items():
                if name not in self._output_name_to_idx:
                    raise RuntimeError(
                        f"Received activation with name {name} at iteration {i}"
                        f", but no such name has been registered. Expected "
                        f"activation names are: "
                        f"{self._output_name_to_idx.values()}"
                    )
                activation = cstorch.from_numpy(tensor)
                activation_map[self._output_name_to_idx[name]] = activation
                received_activations[name] = activation

        self.tracker_execute.stop("recv_first_activation")
        self.tracker_execute.stop("execute_till_recv_loss")

        return received_activations

    def receive_output(self, iteration, name):
        out = super().receive_output(iteration, name)

        self.tracker_execute.stop("recv_first_activation")
        self.tracker_execute.stop("execute_till_recv_loss")

        return out

    def save_initial_state(self, initial_state_dict: dict) -> Union[str, None]:
        if not initial_state_dict:
            return None

        backend = current_backend_impl()

        initial_state_file = os.path.join(
            backend.device.device_data_dir,
            (
                f"initial_state_{self._initial_ckpt_id}.hdf5"
                if self._initial_ckpt_id
                else "initial_state.hdf5"
            ),
        )
        self._initial_ckpt_id += 1

        if os.path.exists(initial_state_file):
            raise FileExistsError(
                f"Initial checkpoint file {initial_state_file} already exists"
            )

        # After all weights were synced (computed) and available, we can
        # save them to the initial checkpoint.
        init_ckpt_dict = {}
        for name, weight in initial_state_dict.items():
            if isinstance(weight, cerebras_pytorch_lib.ApplianceInfo):
                # Special case to handle weights that needs to be carried over.
                init_ckpt_dict[name] = weight
            elif weight.is_tensor_available:
                try:
                    tensor = lazy_tensor_data_wrapper(weight)
                    if isinstance(tensor, DeferredTensor):
                        # Deferred tensors are created using `torch.empty()`
                        # which allocates virtual memory. But since the empty
                        # storage is never actually accessed in a defered
                        # tensor, we close that storage here to avoid spikes
                        # in virtual memory which may lead to OOM during fork.
                        cerebras_pytorch_lib.close_tensor_storage(tensor)

                    init_ckpt_dict[name] = tensor
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to get initial data for {name}"
                    ) from e
            else:
                raise RuntimeError(
                    f"Weight tensor \"{name}\" can not be saved to initial checkpoint as it is not available."
                )

        # We intermittently see HDF5 locking failures here. It's not clear what's
        # causing it, but given that `initial_state_file` is guaranteed to be unique
        # and only written to here, disabling file locking is ok.
        with cstorch.storage.serializers.use_external_link(
            value=True
        ), hdf5_locking(
            value=False
        ), cstorch.storage.serializers.saving_initial_state(
            value=True
        ):
            cstorch.save(init_ckpt_dict, initial_state_file)

        del init_ckpt_dict

        return initial_state_file

    # pylint: disable=arguments-differ
    def compile(
        self,
        batch_size: int,
        cirh_str: str,
        cross_compile_state: Optional[CrossCompileState] = None,
        validate_only: bool = False,
    ):
        """
        Send a compile request to the coordinator.
        """
        with self.tracker_execute.entry("compile"):
            with self.tracker_execute.entry("pt_cirh"):
                if validate_only:
                    logging.info("Compile validated locally")
                    return None

                compile_request = CompileRequest(
                    cirh_content=cirh_str,
                    compile_dir=str(self._compile_dir),
                    batch_size=batch_size,
                    num_csx=self.num_csx,
                    max_wgt_servers=self.max_wgt_servers,
                    num_workers_per_csx=self.num_workers_per_csx,
                    max_act_per_csx=self.max_act_per_csx,
                    # Each CompileRequest is associated with a UUID, which
                    # is used to identify the request in the appliance during
                    # retries.
                    compile_id=str(uuid.uuid4()),
                )
                if cross_compile_state is not None:
                    compile_request.cross_compile_state.CopyFrom(
                        cross_compile_state
                    )

            return super().compile(compile_request)

    def execute_prep(
        self,
        cleanup_stack: ExitStack,
        init_request: Optional[InitRequest] = None,
    ) -> dict:
        """Prepare for execution and return the exe job details"""
        with self.tracker_execute.entry("execute_prep_details"):
            mgmt_client = cleanup_stack.enter_context(
                ClusterManagementClient(
                    tracker_execute=self.tracker_execute,
                    **self._mgmt_client_args,
                )
            )
            self.is_sidecar_available = mgmt_client.is_sidecar_available()
            response = self.request_execute_job(mgmt_client, self._compile_resp)
            self.stage_execute_coordinator(response)

            cleanup_stack.enter_context(self.subscribe(ValidTopics.STALL))

            # From this point on, if we error out, we try to do a clean exit
            cleanup_stack.enter_context(
                self.clean_shutdown(mgmt_client, response['job_id'])
            )

        with self.tracker_execute.entry("execute_init_transfer_setup"):
            self.initialize_servers(init_request)
        return response

    def execute_session(
        self,
        initial_state_dict: Dict[str, Any] = None,
        appliance_weights: Dict[str, Any] = None,
        send_weights_grouper: Optional[TensorGrouper] = None,
        has_modified_seed: Optional[bool] = None,
    ):
        """Prepares weights and starts execution.

        Args:
            initial_state_dict: Weights that needs to be sent to the appliance.
            appliance_weights: Weights that need to be carried over from PTR.
            send_weights_grouper: Callable to process TensorSendPayloads into TensorGroups
        """
        tensor_rt_groups = self.grpc_client.send_check(
            0, info_type=SendCheckRequest.InfoType.GROUP
        )

        rt_initial_state_dict = (
            {
                self._map_wgt_name_fw_to_rt(fw_name): (fw_name, weight)
                for fw_name, weight in initial_state_dict.items()
            }
            if initial_state_dict
            else {}
        )

        rt_appliance_weights = (
            {
                self._map_wgt_name_fw_to_rt(fw_name): (fw_name, info)
                for fw_name, info in appliance_weights.items()
            }
            if appliance_weights
            else {}
        )

        self._sparsity_mask_names = set()

        skipped_weights = set()

        for group in tensor_rt_groups:
            tensor_names = group.tensor_names
            if len(tensor_names) <= 1:
                continue

            # Make an assumption that first tensor in the group is a sparsity mask
            sparsity_mask, _weights = tensor_names[0], tensor_names[1:]
            self._sparsity_mask_names.add(sparsity_mask)

            # Check if all tensors from the group are either in initial checkpoint or in the appliance,
            # otherwise, we need to send all tensors from the group to the appliance.
            if all(name in rt_initial_state_dict for name in tensor_names):
                continue

            if all(name in rt_appliance_weights for name in tensor_names):
                # We do not carry over sparsity mask if it wasn't changed.
                fw_name, _ = rt_appliance_weights[sparsity_mask]
                skipped_weights.add(fw_name)
                del rt_appliance_weights[sparsity_mask]
                continue

            for name in tensor_names:
                if name in rt_appliance_weights:
                    rt_initial_state_dict[name] = rt_appliance_weights[name]
                    del rt_appliance_weights[name]

        # Bake remaining apliances weights into initial_state_dict, so they can be
        # carried over to the next session.
        for rt_name, (fw_name, data) in rt_appliance_weights.items():
            rt_initial_state_dict[rt_name] = (
                fw_name,
                data.get_appliance_info(),
            )

        # The final dictionary that contains the weights that will be sent to the appliance
        # or carried over from the previous session.
        initial_weights = {
            fw_name: weight
            for fw_name, weight in rt_initial_state_dict.values()
        }

        out = super().execute_session(
            initial_weights,
            skipped_weights,
            send_weights_grouper,
            has_modified_seed,
        )

        # Update ApplianceInfo with InBuffer state after we sent/carried over
        # all the weight to the appliance.
        for data in (appliance_weights or {}).values():
            data.get_appliance_info().state = (
                cerebras_pytorch_lib.ApplianceInfoState.InBuffer
            )

        self._skipped_weights -= self._sparsity_mask_names
        return out

    def execute(
        self,
        run_request: RunRequest,
        cleanup_stack: ExitStack,
        initial_state_dict: Dict[str, Any] = None,
        appliance_weights: Dict[str, Any] = None,
        send_weights_grouper: Optional[TensorGrouper] = None,
        has_modified_seed: Optional[bool] = None,
    ):
        """Run a model on the appliance."""
        self.tracker_execute.start("execute_till_recv_loss")

        if not self._exec_prep_is_done:
            from cerebras.appliance.storage.s3_storage import (
                get_boto_session,
                get_s3_client,
            )

            session = get_boto_session()
            credentials = session.get_credentials()

            init_request = None
            if credentials is not None:
                credentials = credentials.get_frozen_credentials()
                credentials = dict(
                    endpoint_url=get_s3_client().meta.endpoint_url,
                    access_key_id=credentials.access_key,
                    secret_access_key=credentials.secret_key,
                    session_token=credentials.token,
                )
                credentials = {
                    k: v for k, v in credentials.items() if v is not None
                }

                init_request = InitRequest(
                    credentials=[
                        InitRequest.Credentials(
                            s3_credentials=InitRequest.Credentials.S3(
                                **credentials
                            )
                        )
                    ]
                )

            self.execute_prep(cleanup_stack, init_request)
            self._exec_prep_is_done = True

        with self.tracker_execute.entry("execute_init_transfer_setup"):
            self.initialize_session(
                run_request,
                self._compile_resp,
                has_modified_seed,
            )
            self.execute_session(
                initial_state_dict,
                appliance_weights,
                send_weights_grouper,
                has_modified_seed,
            )

        self.tracker_execute.start("recv_first_activation")

    def send_weights(
        self,
        initial_weights: Optional[dict] = None,
        skipped_weights: Optional[Set[str]] = None,
        grouper: Optional[TensorGrouper] = None,
    ):
        self._sent_weights.clear()
        self._transferred_weights.clear()

        tensor_rt_groups = self.grpc_client.send_check(
            0, info_type=SendCheckRequest.InfoType.GROUP
        )

        tensor_rt_name_group_map = {}
        tensor_id_group_map = {}
        tensor_id_rt_name_map = {}
        group_map = {}

        @dataclass
        class Group:
            group_id: int
            tensor_names: List[str]

            @dataclass
            class NameID:
                tensor_name: str
                tensor_id: Union[int, str]

            tensor_name_id_pairs: List[NameID]

        for i, group in enumerate(tensor_rt_groups):
            if not group.HasField("group_id"):
                # This must be the mock model case
                # We treat the name as the id in this case
                group = Group(
                    group_id=i,
                    tensor_names=list(group.tensor_names),
                    tensor_name_id_pairs=[
                        Group.NameID(name, name) for name in group.tensor_names
                    ],
                )
            else:
                group = Group(
                    group_id=group.group_id,
                    tensor_names=list(group.tensor_names),
                    tensor_name_id_pairs=[
                        Group.NameID(p.tensor_name, p.tensor_id)
                        for p in group.tensor_name_id_pairs
                    ],
                )

            group_map[group.group_id] = group

            # This is a sanity check, we should always have at least one pair
            assert len(group.tensor_name_id_pairs) != 0

            for p in group.tensor_name_id_pairs:
                tensor_rt_name_group_map[p.tensor_name] = group
                tensor_id_group_map[p.tensor_id] = group
                tensor_id_rt_name_map[p.tensor_id] = p.tensor_name

        tensor_rt_names = set(tensor_rt_name_group_map)
        send_all = (
            len(tensor_rt_name_group_map) == 1
            and list(tensor_rt_names)[0] == self.SEND_ALL_WGTS
        )
        if send_all:
            tensor_rt_names = set()

        from cerebras.appliance.storage import S3Reader
        from cerebras.pytorch.storage.serializers import (
            DeferredFullTensor,
            DeferredGraphTensor,
            DeferredTorchTensor,
        )
        from cerebras.pytorch.storage.utils import lazy_tensor_data_wrapper

        skipped_weights = skipped_weights or set()

        weight_map = {}
        for key, weight in initial_weights.items():
            rt_name = self._map_wgt_name_fw_to_rt(key)

            if rt_name in tensor_rt_names or send_all:
                weight_map[rt_name] = weight
            else:
                skipped_weights.add(key)

        self._skipped_weights = skipped_weights

        def is_s3(t):
            return isinstance(
                t, DeferredTorchTensor
            ) and S3Reader.is_valid_path(t.deferred._path)

        def is_full_or_s3(t):
            return isinstance(t, DeferredFullTensor) or is_s3(t)

        def should_send_deferred(tensors):
            total_args_size = 0
            for _, t in tensors:
                if isinstance(t, DeferredGraphTensor):
                    if not self.is_sidecar_available:
                        # If the sidecar is not available, we can't send the graph
                        # tensor, so it has to be sent using the legacy path
                        return False

                    total_args_size += sum(
                        a.nbytes
                        for a in t._args
                        if isinstance(a, torch.Tensor) and not is_full_or_s3(a)
                    )
                elif is_full_or_s3(t):
                    # If the tensor is a full tensor or an S3 tensor, its size
                    # is negligible, so we don't have to account for it here.
                    pass
                else:
                    # If any one of the tensors in the group is none of the above,
                    # then we have to send the entire group using the legacy path
                    return False

            # If the sum of the argument sizes exceeeds the max transfer bytes,
            # we have to do some tensor chunking and thus cannot use the faster
            # wgt init on memx path.
            # Note, we add about 5MB to the total arg size to account for the
            # other overhead and reduce the chance of going over the message
            # size limit
            return (
                total_args_size + 5 * 1024 * 1024
            ) < cstorch.backends.csx.performance.max_transfer_bytes

        futures = {}
        cancel_grpc = Event()

        # Callback to cancel futures on SIGINT
        def cancel_futures(*args, **kwargs):
            for future in futures.values():
                future.cancel()
            cancel_grpc.set()

        with ExitStack() as exit_stack:
            progress = None
            # Only enable progress bar on TTY
            if sys.stdout.isatty():
                progress = exit_stack.enter_context(
                    tqdm(
                        total=len(weight_map),
                        desc="Sending initial weights",
                        dynamic_ncols=True,  # Match console width
                        unit=" tensors",
                        file=sys.stdout,
                    )
                )
                # Used to safely update progress bar from multiple threads
                progress_lock = Lock()

            num_workers = cstorch.backends.csx.performance.transfer_processes

            eager_executor = exit_stack.enter_context(
                ThreadPoolExecutor(max_workers=num_workers)
            )
            exit_stack.enter_context(on_sigint(cancel_futures))
            # Even if no sigint encountered, cancel all futures on exit
            exit_stack.callback(cancel_futures)

            def carry_over_from_ptr(rt_name, tensor_id):
                self.grpc_client.carry_over_from_ptr(
                    iteration=0,
                    tensor_name=rt_name,
                    tensor_id=tensor_id,
                    keep_in_repo=False,
                )
                if progress is not None:
                    with progress_lock:
                        progress.update(1)

            # Send tensors to the appliance using the legacy gRPC path
            def send_group(tensors):
                for rt_name, t in tensors:
                    scalar_broadcast = isinstance(t, DeferredFullTensor)
                    if scalar_broadcast:
                        t = np.array(t._value, dtype=torch_to_np_dtype(t.dtype))
                    else:
                        t = cstorch.to_numpy(t)

                    self.grpc_client.send_weight(
                        0, rt_name, t, scalar_broadcast, cancel_grpc
                    )

                    if progress is not None:
                        with progress_lock:
                            progress.update(1)

            @contextmanager
            def ingest_weights(tensor_id_shard_id):
                responses = self.grpc_client.start_weight_ingestion(
                    tensor_id_shard_id
                )
                responses_iterator = iter(responses)
                # Make sure to get a response back first before sending the tensors
                next(responses_iterator)

                yield

                for _ in responses_iterator:
                    if progress is not None:
                        with progress_lock:
                            progress.update(1)

            deferred_tensors = defaultdict(dict)
            for group_id, group in group_map.items():
                weights = [
                    (rt_name, weight_map.get(rt_name))
                    for rt_name in group.tensor_names
                ]

                # Keep track of all weights that are sent to the appliance
                self._sent_weights.update(
                    rt_name for rt_name, w in weights if w is not None
                )

                if any(
                    isinstance(w, cerebras_pytorch_lib.ApplianceInfo)
                    for _, w in weights
                ):
                    if not all(
                        isinstance(w, cerebras_pytorch_lib.ApplianceInfo)
                        for _, w in weights
                        if w is not None
                    ):
                        raise RuntimeError(
                            f"Not all weights in group {group_id} are being carried over"
                        )

                    for rt_name, weight in weights:
                        if weight is not None:
                            futures[rt_name] = eager_executor.submit(
                                carry_over_from_ptr, rt_name, weight.uid
                            )

                    continue

                if any(w is None for _, w in weights):
                    raise RuntimeError(
                        f"Group {group_id} has missing weights:\n\t"
                        f"{[rt_name for rt_name, w in weights if w is None]}"
                    )

                self._transferred_weights.update(
                    rt_name for rt_name, _ in weights
                )

                tensors = [
                    (rt_name, lazy_tensor_data_wrapper(w))
                    for rt_name, w in weights
                ]

                if (
                    not self._debug_args.debug_usr.force_send_weights
                    and not cstorch.backends.csx.debug.async_parallel_compute
                    and should_send_deferred(tensors)
                ):
                    deferred_tensors[group_id] = {
                        name: t for name, t in tensors
                    }
                else:
                    futures[tuple(group.tensor_names)] = eager_executor.submit(
                        send_group, tensors
                    )

            if deferred_tensors:
                cluster_details = ClusterDetailsParser(
                    self._compile_resp.cluster_details
                )
                try:
                    # TODO: This should really be number of wgt coordinators
                    num_wgt_servers = cluster_details.extract_num_wgt_srvs()
                except Exception:
                    num_wgt_servers = 1

                def get_weight_ids(group_id):
                    # All (non-mask) tensors belonging to the same group need to
                    # be assigned to the same shard
                    weight_ids = tuple(
                        p.tensor_id
                        for p in group_map[group_id].tensor_name_id_pairs
                    )
                    if len(weight_ids) > 1:
                        # This is the sparsity case. We remove the mask id
                        # from the weight id list as it is not a weight
                        weight_ids = weight_ids[1:]
                    return weight_ids

                if num_wgt_servers == 1:
                    tensor_id_shard_id = [
                        (weight_id, 0)
                        for group_id, _ in deferred_tensors.items()
                        for weight_id in get_weight_ids(group_id)
                    ]
                else:
                    tensor_id_shard_id = assign_tensor_ids_to_shards(
                        {
                            get_weight_ids(group_id): reduce(
                                lambda cost1, cost2: {
                                    k: cost1[k] + cost2[k] for k in cost1
                                },
                                (
                                    (
                                        cerebras_pytorch_lib.estimate_compute_memory_cost(
                                            t._jit_graph
                                        )
                                        if isinstance(t, DeferredGraphTensor)
                                        else {
                                            "total_cpu_time": 0,
                                            "total_memory": prod(t.shape),
                                            "max_memory": prod(t.shape),
                                        }
                                    )
                                    for t in tensors.values()
                                ),
                            )
                            for group_id, tensors in deferred_tensors.items()
                        },
                        num_wgt_servers,
                    )

                def send_tensor_ids(shards):
                    seen = set()
                    for tensor_id, shard_id in tensor_id_shard_id:
                        if cancel_grpc.is_set():
                            return

                        if shard_id not in shards or tensor_id in seen:
                            continue

                        group = tensor_id_group_map[tensor_id]

                        # NOTE: Its important for all tensors in the same group
                        # to be sent to the same shard
                        # NOTE: Also important to send the tensors in the same
                        # order as in the tensor mapping
                        tensors = []
                        tensor_names = []
                        for p in group.tensor_name_id_pairs:
                            deferred_tensor = deferred_tensors[group.group_id][
                                p.tensor_name
                            ]
                            self.logger.debug(
                                f"Sending deferred tensor {p.tensor_name} "
                                f"(shape={list(deferred_tensor.shape)}, "
                                f"dtype={deferred_tensor.dtype}, "
                                f"nbytes={deferred_tensor.nbytes})"
                            )

                            tensor = SendDeferredInputRequest.Tensor(
                                shape=tuple(deferred_tensor.shape),
                                dtype=rtfx_dtype_from_np_dtype(
                                    torch_to_np_dtype(deferred_tensor.dtype)
                                ),
                            )
                            if isinstance(p.tensor_id, str):
                                tensor.tensor_name = p.tensor_id
                            else:
                                tensor.tensor_id = p.tensor_id

                            if isinstance(deferred_tensor, DeferredGraphTensor):
                                tensor.graph_tensor.graph = (
                                    deferred_tensor._jit_graph
                                )
                                for i, arg in enumerate(deferred_tensor._args):
                                    graph_arg = tensor.graph_tensor.args.add()
                                    graph_arg.shape.extend(tuple(arg.shape))
                                    graph_arg.dtype = torch_to_rtfx_dtype(
                                        arg.dtype
                                    )
                                    if isinstance(arg, DeferredFullTensor):
                                        graph_arg.scalar_broadcast_tensor.value.CopyFrom(
                                            np_array_to_rtfx_scalar(
                                                np.array(
                                                    arg._value,
                                                    dtype=torch_to_np_dtype(
                                                        arg.dtype
                                                    ),
                                                )
                                            )
                                        )
                                    elif is_s3(arg):
                                        graph_arg.s3_tensor.path = str(
                                            arg.deferred._path
                                        )
                                        graph_arg.s3_tensor.key = (
                                            arg.deferred._key
                                        )
                                        graph_arg.s3_tensor.index = (
                                            arg.deferred._index
                                        )
                                    elif isinstance(arg, torch.Tensor):
                                        graph_arg.rtfx_tensor.CopyFrom(
                                            np_array_to_rtfx_proto(
                                                cstorch.to_numpy(arg)
                                            )
                                        )
                                    else:
                                        raise TypeError(
                                            f"Found unsupported deferred graph tensor arg type "
                                            f"for {p.tensor_name} arg {i}: {type(arg)}"
                                        )

                            elif isinstance(
                                deferred_tensor, DeferredFullTensor
                            ):
                                tensor.scalar_broadcast_tensor.value.CopyFrom(
                                    np_array_to_rtfx_scalar(
                                        np.array(
                                            deferred_tensor._value,
                                            dtype=torch_to_np_dtype(
                                                deferred_tensor.dtype
                                            ),
                                        )
                                    )
                                )
                            elif isinstance(
                                deferred_tensor, DeferredTorchTensor
                            ):
                                parsed = S3Reader.parse_path(
                                    deferred_tensor.deferred._path
                                )
                                bucket = parsed["bucket"]
                                key = "/".join(
                                    (
                                        parsed["key"],
                                        deferred_tensor.deferred._key,
                                    )
                                )

                                tensor.s3_tensor.bucket = bucket
                                tensor.s3_tensor.key = key
                                tensor.s3_tensor.index = 0
                            else:
                                raise TypeError(
                                    f"Found unsupported deferred tensor type "
                                    f"for {p.tensor_name}: {type(deferred_tensor)}"
                                )

                            tensors.append(tensor)
                            tensor_names.append(p.tensor_name)

                            seen.add(p.tensor_id)

                        self.grpc_client.send_deferred_tensor_group(
                            0, tensors, tensor_names, shard_id
                        )

                buckets = [[] for i in range(num_workers)]
                for shard_id in range(num_wgt_servers):
                    buckets[shard_id % len(buckets)].append(shard_id)

                tensor_names = [[] for i in range(num_workers)]
                for tensor_id, shard_id in tensor_id_shard_id:
                    tensor_names[shard_id % len(tensor_names)].append(
                        tensor_id_rt_name_map[tensor_id]
                    )

                exit_stack.enter_context(ingest_weights(tensor_id_shard_id))

                deferred_executor = exit_stack.enter_context(
                    ThreadPoolExecutor(
                        max_workers=min(num_workers, num_wgt_servers)
                    )
                )
                for bucket, names in zip(buckets, tensor_names):
                    futures[tuple(names)] = deferred_executor.submit(
                        send_tensor_ids, bucket
                    )

            # Wait for all futures to complete
            _, pending = wait(futures.values(), return_when=FIRST_EXCEPTION)

            success = []
            dropped = []
            exc = None
            for k, f in futures.items():
                if not isinstance(k, tuple):
                    k = (k,)

                if (e := f.exception()) is None:
                    success.extend(k)
                    continue
                elif isinstance(e, ApplianceTensorDropped):
                    dropped.extend(k)
                    continue  # Track but don't raise early for dropped tensors

                k = ", ".join(map(str, k))
                if isinstance(e, ApplianceResourceExhausted):
                    self.logger.error(
                        f"Resource exhausted when transferring '{k}'. {str(e)}"
                    )
                else:
                    self.logger.error(
                        f"Ran into error when transferring '{k}'. {str(e)}"
                    )

                exc = e
                break  # Stop to raise on the first error found (early abort)

            # Cancel all pending futures
            def _cancel_pending():
                for p in pending:
                    p.cancel()

            if exc is not None:
                _cancel_pending()
                raise exc

            if success and dropped:
                _cancel_pending()

                raise ApplianceClientException(
                    f"Some weights were successfully transferred, while some were "
                    f"dropped at the coordinator. This indicates an "
                    f"internal error.\n"
                    f"Transferred Tensors: {success}\n"
                    f"Dropped Tenors: {dropped}"
                )
            if dropped:
                _cancel_pending()

                raise ApplianceDropModeComplete(
                    f"All {len(dropped)} weight tensors were dropped."
                )

    def host_inference(
        self,
        checkpoint_filenames: List[str],
        checkpoint_kwargs: dict,
        cleanup_stack: ExitStack,
        draft_compile_response: Optional[CompileResponse] = None,
        num_draft_models: int = 1,
        draft_checkpoint_filenames: List[str] = None,
        draft_checkpoint_kwargs: Optional[dict] = None,
        tokenizer_info: Optional[TokenizerInfo] = None,
    ):
        """Host an inference model in the appliance and return the wsjobid."""

        num_csx_for_draft_inference = 0
        if draft_compile_response:
            TaskType = ClusterDetails.TaskInfo.TaskType
            # First, get the number of WSE in the target compile, we'll offset
            # all wse_id by this number in the draft compile.
            target_num_wse = 0
            for task in self.compile_resp.cluster_details.tasks:
                if task.task_type == TaskType.WSE:
                    target_num_wse = len(task.task_map)

            def get_draft_task_map(task_type):
                for task in draft_compile_response.cluster_details.tasks:
                    if task.task_type == task_type:
                        return task.task_map

            num_csx_for_draft_inference = len(get_draft_task_map(TaskType.WSE))

            # Modify compile_resp.cluster_details!
            add_tasks = (TaskType.WSE, TaskType.ACT, TaskType.CHF)
            for task in self.compile_resp.cluster_details.tasks:
                if task.task_type in add_tasks:
                    c = len(task.task_map)
                    draft_task_map = get_draft_task_map(task.task_type)
                    for i in range(num_draft_models):
                        for dt in draft_task_map:
                            new = task.task_map.add()
                            # Copy from draft model task_map entirely.
                            new.CopyFrom(dt)
                            # Offset each of task_id
                            new.task_id.task_id += c
                            c += 1

                            # Offset all the wse_id from the original target
                            new.task_id.wse_id += target_num_wse
                            for i, wse_id in enumerate(new.task_id.wse_ids):
                                new.task_id.wse_ids[i] = wse_id + target_num_wse

        init_request = InitRequest(
            inference=True,
            num_csx_for_draft_inference=num_csx_for_draft_inference,
        )
        details = self.execute_prep(cleanup_stack, init_request=init_request)

        with self.tracker_execute.entry("execute_load_request"):
            self.grpc_client.load_rtir(
                LoadRequest(
                    cache_compile_dir=self.compile_resp.cache_compile_dir,
                    inference=True,
                    drop_cmd_state=True,
                )
            )

            if num_csx_for_draft_inference:
                cache_compile_dir = draft_compile_response.cache_compile_dir
                self.grpc_client.load_rtir(
                    LoadRequest(
                        cache_compile_dir=cache_compile_dir,
                        inference=True,
                        num_draft_models=num_draft_models,
                        drop_cmd_state=True,
                    )
                )

        if checkpoint_filenames:
            with self.tracker_execute.entry("execute_send_weights"):
                self.logger.info("About to send weights")
                self.send_weights_from_checkpoints(
                    checkpoint_filenames,
                    checkpoint_reader_kwargs=checkpoint_kwargs,
                )
                if draft_checkpoint_filenames:
                    self.logger.info("About to send draft model weights")
                    self.send_weights_from_checkpoints(
                        draft_checkpoint_filenames,
                        checkpoint_reader_kwargs=draft_checkpoint_kwargs,
                    )
                self.logger.info("Finished sending weights")

        with self.tracker_execute.entry("execute_start_streaming"):
            self.logger.info("Finalizing appliance staging for the run")
            # Wait for programming to finish
            self.start_streaming()
            # Wait for iteration 0 to run
            self.grpc_client.run_inference(
                RunInferenceRequest(tokenizer_info=tokenizer_info)
            )
            self.logger.info("Appliance staging is complete")
        return details

    def move_to_ptr(self, tensor_name: str, tensor_id: int) -> None:
        """Move a tensor to PTR which makes is available for the next session."""
        rt_name = self._map_wgt_name_fw_to_rt(tensor_name)
        return super().move_to_ptr(rt_name, tensor_id)

    def get_from_ptr(
        self, name: str, tensor_id: int, keep_in_repo: bool = False
    ):
        """Get a tensor from PTR."""
        return super().get_from_ptr(tensor_id, keep_in_repo)

    def construct_debug_args(self) -> DebugArgs:
        debug_args = super().construct_debug_args()

        # TODO: Conditionlize this on whether we actually need to send any
        #       deferred tensors
        if (
            self.is_sidecar_available
            and not cstorch.backends.csx.debug.async_parallel_compute
        ):
            debug_args.debug_mgr.weight_sidecar.strategy = (
                DebugArgs.DebugMGR.UserSidecar.STRATEGY_ENABLED
            )

        # Populate the visit_fn_map in the debug_args so that they
        # can be propagated to the workers
        for (
            serialized_types,
            serialized_visit_fn,
        ) in serialize_visit_fns().items():
            debug_args.debug_wrk.visit_fn_map[serialized_types] = (
                serialized_visit_fn
            )

        return debug_args

    def compute_compile_hash(
        self,
        cirh_str: str,
        batch_size: int,
        cross_compile_state: CrossCompileState,
    ):
        """
        Compute the hash for the compile request. When modifying this function,
        please make sure that the hashing logic is in sync with logic in CRD.
        Note that the purpose of this function is to define a compile hash
        which is going to be used only locally (within this process), so we
        doesn't include static information (like fabric info, release id, etc.)
        to compute the hash.
        """
        checksum = [
            cirh_str,
            self._debug_args.debug_crd.stop_compile_at,
            self._debug_args.debug_crd.autogen_policy,
            self._debug_args.debug_crd.numeric_config,
            self._debug_args.debug_crd.disable_ws_incremental_compile,
            self._debug_args.debug_crd.disable_autogen_leftover_conversion,
            self.num_csx,
            batch_size,
            self.max_wgt_servers,
            self.max_act_per_csx,
            cross_compile_state,
        ]
        return hash("".join([str(item) for item in checksum]))

    @property
    def _checkpoint_reader_cls(self):
        return self.checkpoint_reader_cls

    def _map_wgt_name_fw_to_rt(self, tensor_name):
        if tensor_name in self.weight_names:
            return self.weight_names[tensor_name]
        if tensor_name in self.auxilliary_state_names:
            return self.auxilliary_state_names[tensor_name]
        return tensor_name

    def save_weights_to_s3(
        self,
        tensors,
        path: str,
        bucket: str,
        key_prefix: str,
        iteration: int,
    ):
        from cerebras.appliance.storage.serializers import DeferredObject
        from cerebras.pytorch.storage.utils import lazy_tensor_data_wrapper

        tensors = {
            cerebras_pytorch_lib.get_tensor_name(t): (k, t)
            for k, t in tensors.items()
        }

        weight_infos = []
        for rt_name, (name, t) in tensors.items():
            if rt_name in self.skipped_weights:
                if t.device.type == "lazy":
                    t = lazy_tensor_data_wrapper(t)
                yield name, t
            elif rt_name not in self.skipped_weights:
                weight_infos.append(
                    (rt_name, tuple(t.shape), torch_to_np_dtype(t.dtype))
                )

        with self.tracker_execute.entry("save_weights", overwrite=True):
            # Send gRPC request to have tensors saved to S3 by weight host
            responses = self.grpc_client.save_weights(
                iteration,
                weight_infos,
                bucket,
                key_prefix,
                compress_data=cstorch.backends.csx.performance.compress_weights,
            )

            for response in responses:
                if response is None:
                    raise RuntimeError(
                        f"Unable to save {name}. Failed to save all weights."
                    )

                k, t = tensors[response.name]

                yield k, DeferredObject(
                    path,
                    response.s3_location.key,
                    response.s3_location.index,
                    metadata={"__TYPE__": "TorchTensorSerializer"},
                    # We don't want to save a copy, we want to save this exact deferred object
                    force_external_link=True,
                )

    def recv_weight(self, tensor, iteration):
        if not isinstance(tensor, torch.Tensor) or tensor.device.type != "lazy":
            # Nothing to receive if tensor is not a lazy torch tensor
            return tensor

        # pylint: disable=c-extension-no-member
        # pylint: disable=no-member
        weight_name = cerebras_pytorch_lib.get_tensor_name(tensor)

        # If there is no weight name, then it is not a weight tensor
        if weight_name is None or weight_name in self.skipped_weights:
            logging.debug(f"Not fetching skipped: {weight_name}")

            from cerebras.pytorch.storage.utils import lazy_tensor_data_wrapper

            return lazy_tensor_data_wrapper(tensor)

        # Get the runtime name of the tensor
        tensor_name = self._map_wgt_name_fw_to_rt(weight_name)

        logging.debug(f"Fetching {tensor_name} at iteration {iteration}")
        return self.grpc_client.recv_output(iteration, tensor_name)

    def save_weights(
        self,
        weights: List[Tuple[str, Union[torch.Tensor, Any]]],
        file_name: str,
        iteration: int,
        fetch_only: bool = False,
    ) -> None:
        """Request weights from appliance and save to the file_name.

        Args:
            weights: List of weights to save. Each weight is a tuple of the
                weight name and the tensor (or other objects) to fetch from
                the appliance and save.
            file_name: Name of the file to save the weights to.
            iteration: Appliance iteration number to save the weights for.
            fetch_only: If True, forces weights fetching from the appliance.
        """

        def get_parameter_name(tensor):
            if (
                isinstance(tensor, torch.Tensor)
                and tensor.device.type == "lazy"
            ):
                # pylint: disable=c-extension-no-member
                # pylint: disable=no-member
                return cerebras_pytorch_lib.get_tensor_name(tensor)
            return getattr(tensor, "_parameter_name", None)

        def get_tensors():
            seen_weights = set()

            # Create a map between the weight name and the external name
            # to handle duplicate weights
            alias_map = defaultdict(list)
            for external_name, obj in weights:
                parameter_name = get_parameter_name(obj)
                if parameter_name is not None:
                    # pylint: disable=protected-access
                    alias_map[parameter_name].append(external_name)

            # external_name: The name seen by the user (what's saved in ckpt)
            # weight_name: The name of the weight in the model
            # tensor_name: The name of the weight seen by the appliance
            for external_name, obj in weights:
                ckpt_indices = [external_name]

                weight_name = get_parameter_name(obj)
                if weight_name is not None:
                    ckpt_indices.extend(
                        alias
                        for alias in alias_map[weight_name]
                        if alias != external_name
                    )
                else:
                    weight_name = external_name

                if weight_name in seen_weights:
                    continue
                else:
                    seen_weights.add(weight_name)

                tensor_name = None

                if isinstance(obj, torch.Tensor):
                    tensor_name = self.weight_names.get(weight_name)

                    if weight_name in self.skipped_weights:
                        logging.debug(f"Not fetching skipped: {weight_name}")
                        if obj.device.type == "lazy":
                            obj = lazy_tensor_data_wrapper(obj)
                        tensor_name = None
                    elif tensor_name is None and obj.device.type == "lazy":
                        tensor_name = weight_name

                    if tensor_name is None:
                        logging.debug(
                            f"Saving tensor {external_name} to indices: {ckpt_indices}"
                        )
                        # Save the object as is
                        yield None, ckpt_indices, obj
                    else:
                        logging.debug(
                            f"Fetching {tensor_name} and saving to indices: {ckpt_indices}"
                        )
                        # Fetch tensor before saving
                        yield tensor_name, ckpt_indices, None
                elif fetch_only:
                    logging.debug(
                        f"Fetching {weight_name} and saving to indices: {ckpt_indices}"
                    )
                    # Fetch tensor before saving
                    yield weight_name, ckpt_indices, None
                else:
                    logging.debug(
                        f"Saving object {external_name} to indices: {ckpt_indices}"
                    )
                    # Save the object as is
                    yield None, ckpt_indices, obj

        recv_tensors = list(get_tensors())

        # Build unique tensor names for validating.
        recv_tensor_names = {name for name, _, _ in recv_tensors}

        # Only use multiprocessing if there are multiple tensors to fetch
        num_processes = min(
            self._transfer_threads,
            sum(1 for x in recv_tensor_names if x is not None),
        )
        num_processes = max(num_processes, 1)

        # Some related tensors should be requested together to minimize peak
        # memory. Each tensor is independent from the other tensors; the
        # grouping is just to control the fetch order.
        recv_groups = []

        # self.recv_groups is a (possibly empty) list of list of tensor names.
        if self.recv_groups:
            # Build a lookup from tensor_name->(tensor_name, indices, obj)
            # the `None` key will have overlaps, but thats fine. All tensors
            # with a name are guaranteed unique.
            recv_tensor_dict = {t[0]: t for t in recv_tensors}

            # For each group of tensor names, build a matching "group" of
            # recv_tensor input (tuples of (name, indices, obj) )
            for group in self.recv_groups:
                recv_group = []
                for tensor_name in group:
                    inputs = recv_tensor_dict.get(tensor_name, None)
                    if inputs is not None:
                        # Move from global recv list to this group.
                        recv_tensors.remove(inputs)
                        recv_group.append(inputs)
                recv_groups.append(recv_group)

        # Each remaining tensor (maybe all of them) is its own group.
        recv_groups.extend([t] for t in recv_tensors)

        transfer_tracker = TensorTransferTracker()

        with self.tracker_execute.entry(
            "Retrieve and Save weights"
        ), limit_mp_threads():
            if num_processes > 1:
                ctx = multiprocessing.get_context('spawn')
                pool_cls = functools.partial(
                    multiprocessing.pool.Pool,
                    context=ctx,
                )
            else:
                ctx = multiprocessing.get_context()
                pool_cls = multiprocessing.dummy.Pool
            with short_temp_dir():
                m = ctx.Manager()
            lock = m.Lock()
            with cstorch.saver.storage.use_cstorch_types(True), pool_cls(
                processes=num_processes,
                initializer=WeightReceiver.initializer,
                initargs=(
                    self._coord_address,
                    self._certificate_bytes,
                    self._default_authority,
                    file_name,
                    iteration,
                    lock,
                ),
            ) as pool:
                iter_recv = itertools.chain.from_iterable(
                    pool.imap_unordered(WeightReceiver.runner, recv_groups)
                )
                for pkl in tqdm(
                    iter_recv,
                    total=len(recv_tensor_names),
                    desc="Transferring weights from server",
                    dynamic_ncols=True,  # Match console width
                    unit=" tensors",
                    file=sys.stdout,
                    disable=None,  # Disable on non-TTY
                ):
                    tensor_name, outcome = WeightReceiver.deserialize(pkl)
                    transfer_tracker.add(tensor_name, outcome)

            transfer_tracker.validate(recv_tensor_names)


class WeightReceiver:
    """A class to use in a multiprocessing context for receiving weights."""

    impl: Optional["WeightReceiver"] = None

    def __init__(
        self,
        coord_address,
        certificate_bytes: Optional[bytes],
        default_authority,
        file_name,
        iteration,
        lock,
    ):
        """Constructs a `WeightReceiver` instance.

        Args:
            coord_address: Address of the coordinator to send to.
            certificate_bytes: Optional PEM encoded certificate byte string for
                grpc secure channel setup.
            default_authority: Authority to authorize communication.
        """
        credentials = None
        if certificate_bytes:
            credentials = grpc.ssl_channel_credentials(certificate_bytes)

        self._grpc_client = ApplianceClient(
            coord_address,
            credentials=credentials,
            default_authority=default_authority,
        )

        self._file_name = file_name
        self._iteration = iteration
        self._writer_lock = lock

        # Add pickling support to exceptions so that they include their
        # traceback
        from tblib import pickling_support

        pickling_support.install()

        # gRPC exceptions are not picklable by default. Register custom picklers
        # so they can be properly pickled to be sent across processes.
        register_grpc_error_pickler()

    def __call__(self, inputs):
        """Downloads the given tensor through gRPC from appliance service."""
        tensor_name = "Unknown"
        ckpt_indices = []
        try:
            tensor_name, ckpt_indices, tensor = inputs
            if tensor_name is not None:
                tensor = self._grpc_client.recv_output(
                    self._iteration, tensor_name
                )

                try:
                    # Make the tensor writable so that we don't have to copy it
                    # in `cstorch.from_numpy()`. Some arrays cannot be modified
                    # so we ignore the error and copy the array instead.
                    tensor.flags.writeable = True
                except Exception:  # pylint: disable=broad-except
                    pass

                tensor = cstorch.from_numpy(tensor)
            with self._writer_lock, hdf5_locking(value=False):
                saver = PyTorchH5Saver()

                def retry(f, *args):
                    attempts = 3
                    delay = 1
                    while attempts:
                        try:
                            return f(*args)
                        except Exception as e:  # pylint: disable=broad-except
                            if isinstance(e, OSError):
                                pass
                            elif isinstance(e.__cause__, OSError):
                                # PyTorchH5Saver.save_tensor() sometimes catches errors and
                                # raises a new error with the original error as the cause.
                                e = e.__cause__
                            else:
                                raise

                            attempts -= 1
                            # See note below on special handling of errno 28.
                            # If we attempt again, it will cause a segfault when file
                            # is closed, causing a hang.
                            if not attempts or e.errno == 28:
                                raise
                            logging.warning(
                                f"Will retry {f.__qualname__} in {delay} seconds. "
                                f"Remaining attempts: {attempts}",
                                exc_info=True,
                            )
                            time.sleep(delay)
                            delay *= 2

                retry(
                    saver.save_tensor, self._file_name, ckpt_indices[0], tensor
                )

                retry(
                    saver.create_links,
                    self._file_name,
                    ckpt_indices[0],
                    ckpt_indices[1:],
                )

            return WeightReceiver.serialize((tensor_name, True))
        except OSError as e:
            # HDF5 has a bug when it hits errno 28 (i.e., "No space left on device")
            # in that it runs into a segfault when closing the open file after OS
            # raises errno 28. Additionally, multiprocessing.pool fails to detect
            # child processes that just die and hangs indefinitely. These 2 issues
            # together cause a hang when we run out of disk space during checkpoint
            # saving. The open HDF5 file is closed _after_ the exception is handled
            # since we open the file for write in a context manager in
            # `PyTorchH5Saver.save_tensor()` and the file is closed in the __exit__()
            # handler. If we can somehow communicate this failure to the master process
            # _before_ the file is closed, the master process knows about the failure
            # and can exit the pool immediately and avoid the hang.
            # In the default case, we catch exceptions, serialize them, and return normally.
            # But by letting the exception pass through in the case of errno 28, the
            # multiprocessing library turns it into a `multiprocessing.pool.RemoteTraceback`
            # and sends it to the master process before the file is closed, working around
            # the hang.
            if e.errno == 28:
                logging.error(
                    f"Ran into error receiving tensor \"{tensor_name}\": {e}"
                )
                raise
            else:
                return WeightReceiver.serialize((tensor_name, e))
        except Exception as e:  # pylint: disable=broad-except
            return WeightReceiver.serialize((tensor_name, e))

    @staticmethod
    def serialize(val):
        """Generic serialization using dill."""
        return dill.dumps(val)

    @staticmethod
    def deserialize(pkl_val):
        """Generic de-serialization method using dill."""
        return dill.loads(pkl_val)

    @staticmethod
    def initializer(*args, **kwargs):
        """The initializer to use in multiprocessing."""
        WeightReceiver.impl = WeightReceiver(*args, **kwargs)

    @staticmethod
    def runner(group):
        """The runner method to use in multiprocessing."""
        assert WeightReceiver is not None, "Initializer must be called."
        # pylint: disable=not-callable
        return [WeightReceiver.impl(inputs) for inputs in group]
