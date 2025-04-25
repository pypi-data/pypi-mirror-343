#!/usr/bin/env python3
# Copyright 2016-2024 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""GRPC Server For weight init/loading."""
import argparse
import logging
import os
import tempfile
import threading
from dataclasses import dataclass, replace
from multiprocessing import resource_tracker
from multiprocessing.shared_memory import SharedMemory
from queue import Empty as EmptyQueue
from queue import Queue
from threading import Lock, Thread
from traceback import format_exception
from typing import Any, Tuple

import numpy as np

import cerebras.pytorch as cstorch
from cerebras.appliance import log
from cerebras.appliance.cluster.cluster_details import ClusterDetailsParser
from cerebras.appliance.data.conversions import np_dtype_from_rtfx_dtype
from cerebras.appliance.pb.framework import appliance_service_pb2_grpc
from cerebras.appliance.pb.framework.appliance_service_pb2 import (
    DoneResponse,
    FinalizeResponse,
    GetOutputResponse,
    InitRequest,
    InitResponse,
    NotifyCrashResponse,
    NotifyStallResponse,
    SendDeferredInputRequest,
    SendDeferredInputResponse,
)
from cerebras.appliance.pb.workflow.appliance.common.common_config_pb2 import (
    ClusterDetails,
    DebugArgs,
    SendToEveryTask,
)
from cerebras.appliance.pb.ws.common_pb2 import (
    WS_RT_INTERNAL_ERROR,
    ClockSyncResponse,
)
from cerebras.appliance.pb.ws.rtfx_pb2 import RtFxProto
from cerebras.pytorch.storage.utils import rtfx_to_torch_dtype
from cerebras.pytorch.utils._app.utils import (
    _proto_msg_from_jsonfile,
    _serve,
    _service_api,
    _setup_logging,
)


def _np_from_rtfx(
    buffer: bytearray, rtfx_dtype: int, shape: Tuple[int]
) -> np.ndarray:
    """Returns a numpy array from the given buffer with the given rtfx dtype.

    Args:
        buffer: The buffer containing the data.
        rtfx_dtype: The RtFxProto dtype.
        shape: The shape of the tensor.
    Returns:
        The numpy array matching the given buffer.
    """
    # Construct np.ndarray
    dtype = np_dtype_from_rtfx_dtype(rtfx_dtype)
    if dtype == bool:  # RtFx T_I1 is stored as 16-bit int
        dtype = np.int16

    if not shape:
        shape = []
    array = np.frombuffer(buffer, dtype=dtype).reshape(shape)

    # I1 comes through as int16, but it _should_ be bool...
    # Might need dtype conversion.
    if rtfx_dtype == RtFxProto.T_I1 and array.dtype != bool:
        array = array.astype(bool)

    return array


@dataclass
class TensorPayload:
    tensor_id: int
    tensor: SendDeferredInputRequest.Tensor.Graph
    shape: tuple
    dtype: Any


@log.named_class_logger("weight.WeightSidecarServicer")
class WeightSidecarServicer(
    appliance_service_pb2_grpc.ApplianceServicer, log.ClassLogger
):
    """Service for initializing and/or loading weights."""

    def __init__(
        self,
        cluster_details: ClusterDetails,
        debug_args: DebugArgs,
        role_id: int,
    ):
        super().__init__()

        self._done_event = threading.Event()
        self._lock = Lock()
        self._tensor_queue = Queue()
        # We set the maxsize to be 3 to avoid the queue from growing too large
        # If runtime consumes the tensors at a slower rate than the producer
        # produces them, we block to avoid computing and having to store too
        # many tensors in memory at once.
        # If runtime consumes tensors at a faster rate than the producer can
        # produce them then, the queue will never reach maximum capacity.
        self._results_queue = Queue(maxsize=3)

        self.thread = None

    def wait(self):
        """Blocks until the server is done."""
        self._done_event.wait()
        if self.thread is not None:
            self.thread.join()

    def __del__(self):
        self.logger.info(f"{self.__class__.__name__} is being destructed.")

    @_service_api()
    def UnaryInit(self, request: InitRequest, context):
        for credentials in request.credentials:
            if credentials.HasField("s3_credentials"):
                s3_credentials = credentials.s3_credentials
                for key in (
                    "endpoint_url",
                    "access_key_id",
                    "secret_access_key",
                    "session_token",
                ):
                    if s3_credentials.HasField(key):
                        os.environ[f"AWS_{key.upper()}"] = getattr(
                            s3_credentials, key
                        )

        def compute_tensors():
            while not self._done_event.is_set():
                try:
                    payload = self._tensor_queue.get(timeout=1)
                except EmptyQueue:
                    continue

                tensor = payload.tensor

                try:
                    self.logger.info(f"Starting to compute {payload.tensor_id}")

                    args = []
                    for i, arg in enumerate(tensor.args):
                        if arg.HasField("rtfx_tensor"):
                            rtfx_proto = arg.rtfx_tensor
                            args.append(
                                cstorch.from_numpy(
                                    _np_from_rtfx(
                                        rtfx_proto.tensor.data,
                                        rtfx_proto.dtype,
                                        rtfx_proto.tensor.shape,
                                    )
                                )
                            )

                        elif arg.HasField("scalar_broadcast_tensor"):
                            from cerebras.pytorch.storage.serializers import (
                                DeferredFullTensor,
                            )

                            args.append(
                                DeferredFullTensor(
                                    tuple(arg.shape),
                                    rtfx_to_torch_dtype(arg.dtype),
                                    _np_from_rtfx(
                                        arg.scalar_broadcast_tensor.value.scalar.data,
                                        arg.dtype,
                                        (),
                                    ).item(),
                                )._to_cpu()
                            )

                        elif arg.HasField("s3_tensor"):
                            from cerebras.appliance.storage.s3_storage import (
                                S3Reader,
                            )
                            from cerebras.appliance.storage.serializers import (
                                DeferredObject,
                            )
                            from cerebras.pytorch.storage.serializers import (
                                DeferredTorchTensor,
                            )

                            s3_tensor = arg.s3_tensor
                            args.append(
                                DeferredTorchTensor(
                                    DeferredObject(
                                        S3Reader.construct(
                                            s3_tensor.path,
                                        ),
                                        s3_tensor.key,
                                        s3_tensor.index,
                                    ),
                                    tuple(arg.shape),
                                    rtfx_to_torch_dtype(arg.dtype),
                                )._to_cpu()
                            )

                    args_msg = ""
                    if args:
                        args_msg = "\n".join(
                            f"\t{tensor.args[i].WhichOneof('arg_impl')} arg {i}: "
                            f"shape={arg.shape}, dtype={arg.dtype}"
                            for i, arg in enumerate(args)
                        )
                        args_msg = f"\nwith args:\n{args_msg}\n"

                    self.logger.info(
                        f"Tensor {payload.tensor_id} has graph:\n{tensor.graph}{args_msg}"
                    )

                    from cerebras.pytorch.storage.serializers import (
                        DeferredGraphTensor,
                    )

                    expected_dtype = rtfx_to_torch_dtype(payload.dtype)

                    result = DeferredGraphTensor(
                        tensor.graph,
                        args,
                        tuple(payload.shape),
                        expected_dtype,
                    )._to_cpu()

                    if (
                        list(result.shape) != list(payload.shape)
                        or result.dtype != expected_dtype
                    ):
                        raise ValueError(
                            f"Expected shape {payload.shape} and dtype {expected_dtype} "
                            f"for tensor {payload.tensor_id}, "
                            f"but got shape {list(result.shape)} and dtype {result.dtype}"
                        )

                    result = replace(payload, tensor=cstorch.to_numpy(result))

                    self.logger.info(
                        f"Computed {result.tensor_id}, "
                        f"shape={result.tensor.shape}, "
                        f"dtype={result.tensor.dtype}"
                    )
                except Exception as e:
                    result = replace(payload, tensor=e)

                self._results_queue.put(result)

        self.thread = Thread(target=compute_tensors)
        self.thread.start()

        return InitResponse()

    @_service_api()
    def UnarySendDeferredInput(
        self, request: SendDeferredInputRequest, context
    ):
        for tensor in request.tensors:
            if tensor.HasField("graph_tensor"):
                self._tensor_queue.put(
                    TensorPayload(
                        tensor_id=tensor.tensor_id,
                        tensor=tensor.graph_tensor,
                        shape=tensor.shape,
                        dtype=tensor.dtype,
                    )
                )

                self.logger.info(
                    f"Received a graph tensor request for tensor: {tensor.tensor_id}"
                )

        return SendDeferredInputResponse()

    @_service_api()
    def UnaryGetOutput(self, request, context):
        self.logger.info(
            f"Received UnaryGetOutput request for tensor: {request.tensor_id}"
        )
        # We always receive results and requests in the same order
        # So, there's no need to cache results. Only if we move
        # to using multiple threads to compute results would we need to
        # check the ordering
        payload = self._results_queue.get()
        result = payload.tensor

        if isinstance(result, Exception):
            self.logger.error(
                "".join(
                    format_exception(type(result), result, result.__traceback__)
                )
            )
            return GetOutputResponse(
                code=WS_RT_INTERNAL_ERROR, message=str(result)
            )

        shm = SharedMemory(name=request.shm_name)

        # Disable mp resource tracking for each shared memory block in order
        # to prevent memory leak warnings when the resource tracker tries
        # to clean up. The weight host is responsible for creating this shared memory
        # region and cleaning it up, whereas in the weight sidecar we only consume it
        # and therefore don't need to track it. (ref: https://bugs.python.org/issue39959)
        # pylint: disable=protected-access
        resource_tracker.unregister(shm._name, 'shared_memory')

        try:
            # Runtime expects booleans as T_I1 which are with 16-bit tensors
            shared_array = np.ndarray(
                result.shape,
                result.dtype if result.dtype != bool else np.uint16,
                buffer=shm.buf,
            )
            np.copyto(shared_array, result, casting="same_kind")

            self.logger.info(
                f"Copied tensor {request.tensor_id} into shared memory"
            )
        except Exception as e:
            self.logger.error(
                "".join(format_exception(type(e), e, e.__traceback__))
            )
            return GetOutputResponse(code=WS_RT_INTERNAL_ERROR, message=str(e))
        finally:
            shm.close()

        return GetOutputResponse()

    @_service_api()
    def UnaryFinalize(self, request, context):
        return FinalizeResponse()

    @_service_api()
    def UnaryNotifyStall(self, request, context):
        return NotifyStallResponse()

    @_service_api()
    def UnaryNotifyCrash(self, request, context):
        return NotifyCrashResponse()

    @_service_api()
    def UnaryDone(self, request, context):
        self._done_event.set()
        return DoneResponse()

    @_service_api()
    def UnaryClockSync(self, request, context):
        return ClockSyncResponse()


def main():
    """Start the weight init/load server."""
    parser = argparse.ArgumentParser(
        "Wafer-Scale Cluster weight init/load service."
    )
    parser.add_argument(
        '-a',
        '--all_details',
        required=True,
        type=str,
        help="Path to file containing json protobuf of SendToEveryTask",
    )
    args = parser.parse_args()

    sent_data = _proto_msg_from_jsonfile(
        SendToEveryTask,
        args.all_details,
        ignore_unknown=True,  # Ignore the `_comment` field.
    )

    _setup_logging(sent_data.debug_args.debug_wgt.log_settings)

    cluster_details_parser = ClusterDetailsParser(sent_data.cluster_details)
    is_swmodel = "swmodel" in cluster_details_parser.extract_cm_address()
    task_type = (
        ClusterDetails.TaskInfo.TaskType.ACT
        if is_swmodel
        else ClusterDetails.TaskInfo.TaskType.WGT
    )

    wse_id, _ = cluster_details_parser.extract_wse_details(
        task_type, sent_data.id
    )[0]

    logging.info("Task details:")
    logging.info(f" Task ID: {sent_data.id}")
    logging.info(f" WSE ID: {wse_id}")

    _serve(
        cluster_details_parser.extract_sidecar_address(task_type, sent_data.id),
        WeightSidecarServicer(
            sent_data.cluster_details,
            sent_data.debug_args,
            sent_data.id,
        ),
    )


if __name__ == "__main__":
    # PyTorch DataLoader in multi-processing mode will try to create sockets
    # with temporary file descriptors when using fork. If the direcotry name
    # is too long, it causes "AF_UNIX path too long". So we reset TMPDIR to
    # avoid these issues.
    tempfile.tempdir = None  # Clear the cached tempdir if it already exists
    os.environ["TMPDIR"] = ""

    main()
