# Copyright 2016-2024 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

import logging
from contextlib import nullcontext
from numbers import Number
from pathlib import Path
from typing import List, Optional

import numpy
import torch
from typing_extensions import Self

import cerebras.pytorch as cstorch
from cerebras.appliance.data.conversions import np_dtype_from_rtfx_dtype
from cerebras.appliance.storage import (
    DeferredObject,
    SerializationContext,
    StorageReader,
    register_serializer,
)
from cerebras.pytorch.backend import current_backend
from cerebras.pytorch.core.appliance_utils import rtfx_to_np_array
from cerebras.pytorch.lib import cerebras_pytorch_lib

# TODO: Move DeferredTensor into this file
from cerebras.pytorch.saver.storage import (
    DeferredTensor as BaseDeferredTensor,  # TODO: Move these into this file
)
from cerebras.pytorch.storage.utils import (
    np_to_torch_dtype,
    torch_to_np_dtype,
    torch_to_rtfx_dtype,
)

from cerebras.pytorch.saver.storage import cache_deferred_tensors  # noqa
from cerebras.pytorch.saver.storage import (  # noqa
    check_deferred_backing_storage,
)
from cerebras.pytorch.saver.storage import saving_initial_state  # noqa
from cerebras.pytorch.saver.storage import use_cstorch_types  # noqa
from cerebras.pytorch.saver.storage import use_external_link  # noqa


def _set_flatten(d):
    return list(d), None


def _set_flatten_with_keys(d):
    values, context = _set_flatten(d)
    return [
        (torch.utils._pytree.SequenceKey(i), v) for i, v in enumerate(values)
    ], context


def _set_unflatten(values, context):
    return set(values)


# Add support for flattening sets
torch.utils._pytree._private_register_pytree_node(
    set,
    _set_flatten,
    _set_unflatten,
    serialized_type_name="builtins.set",
    flatten_with_keys_fn=_set_flatten_with_keys,
)


@register_serializer(torch.Tensor)
class TorchTensorSerializer:
    @staticmethod
    def serialize(tensor, context):
        backend = current_backend(False, False)

        if backend is not None:
            cpu_tensor = backend.to_cpu(tensor)
        else:
            cpu_tensor = tensor.to("cpu")

        if isinstance(cpu_tensor, torch.Tensor):
            context.metadata["__TORCH__"] = True
            # shape metadata is expected to be a list of tuples
            context.metadata["shapes"] = [tuple(cpu_tensor.shape)]
            context.metadata["dtypes"] = [str(cpu_tensor.dtype)]
            context.metadata["rtfx_dtypes"] = [
                torch_to_rtfx_dtype(cpu_tensor.dtype)
            ]

            if not isinstance(cpu_tensor, DeferredTensor):
                # Dump value in a format that is compatible with RtFxProto
                # Note, don't further serialize the numpy array as that causes
                # issues when loading on the appliance due to what metadata
                # gets saved alongside the object
                return cstorch.to_numpy(cpu_tensor)

        return context.serialize(cpu_tensor)

    @staticmethod
    def deserialize(value, context):
        if isinstance(value, (DeferredTorchTensor, DeferredTensor)):
            return value

        if context.metadata.get("__RTFX__"):
            shape = context.metadata["shapes"][0]
            rtfx_dtype = context.metadata["rtfx_dtypes"][0]
            return cstorch.from_numpy(
                rtfx_to_np_array(value.getbuffer(), shape, rtfx_dtype)
            )

        shape = context.metadata["shapes"][0]
        if "dtypes" in context.metadata:
            _, dtype = context.metadata["dtypes"][0].split(".")
            dtype = getattr(torch, dtype)
            np_dtype = torch_to_np_dtype(dtype)
        else:
            np_dtype = np_dtype_from_rtfx_dtype(
                context.metadata["rtfx_dtypes"][0]
            )
            dtype = np_to_torch_dtype(np_dtype)

        if isinstance(value, DeferredObject):
            return DeferredTorchTensor(value, shape, dtype)

        return cstorch.from_numpy(value.astype(np_dtype))


class DeferredTensor(BaseDeferredTensor):
    def serialize(self, context: SerializationContext):
        if self._is_dirty:
            context.metadata["shapes"] = [tuple(self.shape)]
            context.metadata["dtypes"] = [str(self.dtype)]
            return context.hoist(context.serialize(self._tensor))
        return self._serialize(context)

    def _serialize(self, context: SerializationContext):
        """Serializes the tensor.

        This is called when the tensor has not been previously not materialized
        on CPU, which means the deferred type can be serialized for further
        retrieval.
        """
        raise NotImplementedError


class SaveTensor(DeferredTensor):
    def __new__(cls, data, path):
        return cls._make_subclass(cls, data, require_grad=False)

    def __init__(self, data, path):
        self._data = data
        self._path = path

    def _to_cpu(self):
        return self._data.to("cpu")


@register_serializer()
class DeferredTorchTensor(DeferredTensor):
    def __new__(cls, deferred, shape, dtype):
        data = torch.empty(shape, dtype=dtype, device="cpu")
        return cls._make_subclass(cls, data, require_grad=False)

    def __init__(self, deferred, shape, dtype):
        super().__init__()

        self.deferred = deferred

        self._stat = self.deferred._reader.stats

    def __getstate__(self):
        clear_cache = False
        stats = self.deferred._reader.stats
        if self._tensor is None and (
            stats is None or _timestamp_changed(stats, self._stat)
        ):
            self._materialize(cache_override=True)
            clear_cache = True

        state = self.__dict__.copy()

        if clear_cache:
            self._tensor = None

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        # If tensor is non-materialized, we need to ensure the backing file still exists and its
        # timestamp hasn't changed from before.
        if self._tensor is None:
            stats = self.deferred._reader.stats
            if stats is None:
                raise RuntimeError(
                    f"Attempting to access a deferred tensor at {stats.path} "
                    f"which no longer exists."
                )
            # Here we're checking against the file stats now vs when the original tensor that was
            # pickled and we loaded into `self._stat` now.
            self._check_file_modification("unpickle")

    def _to_cpu(self):
        value = self.deferred.value
        if isinstance(value, numpy.ndarray):
            return cstorch.from_numpy(value)
        return value

    def _clone(self) -> Self:
        # Use the file descriptor, since the filepath may have been unlinked. But since we hold the
        # descriptor open, the file itself hasn't been deleted.
        self._check_file_modification("clone")
        cloned = DeferredTorchTensor(self.deferred, self.shape, self.dtype)
        cloned.requires_grad = self.requires_grad
        return cloned

    def _check_file_modification(self, action: str):
        """Check whether the backing file has been modified since the tensors was created."""
        _check_file_modification(
            self.deferred._reader.stats,  # Get latest stat
            self._stat,  # Stored stat when object was first created
            f"{action} deferred tensor with key \"{self.deferred._key}\" from {self.deferred._reader.path}",
        )

    def _serialize(self, context):
        context.metadata["shapes"] = [tuple(self.shape)]
        context.metadata["dtypes"] = [str(self.dtype)]
        return context.serialize(self.deferred)

    @staticmethod
    def deserialize(value, context):
        if isinstance(value, DeferredTorchTensor):
            return value

        shape = context.metadata["shapes"][0]
        _, dtype = context.metadata["dtypes"][0].split(".")
        dtype = getattr(torch, dtype)

        return DeferredTorchTensor(value, shape, dtype)


@register_serializer()
class DeferredFullTensor(DeferredTensor):
    def __new__(
        cls,
        size: torch.Size,
        dtype: Optional[torch.dtype] = None,
        value: Optional[Number] = None,
    ):
        data = torch.empty(size, dtype=dtype, device="cpu")
        return cls._make_subclass(cls, data, require_grad=False)

    def __init__(
        self,
        size: torch.Size,
        dtype: Optional[torch.dtype] = None,
        value: Optional[Number] = None,
    ):
        """Constructs a `DeferredFullTensor` instance.

        Args:
            size: The size of the tensor.
            dtype: The data type of the tensor. If not specified, defaults to
                the default torch dtype.
            value: The value to fill the tensor with. If not specified, defaults
                to uninitialized data.
        """
        super().__init__()

        self._value = value

    @property
    def fill_value(self) -> Number:
        """Returns the fill value."""
        return self._value

    def _to_cpu(self) -> torch.Tensor:
        if self._value is None:
            return torch.empty(self.shape, dtype=self.dtype)
        elif self._value == 0:
            return torch.zeros(self.shape, dtype=self.dtype)
        elif self._value == 1:
            return torch.ones(self.shape, dtype=self.dtype)
        else:
            return torch.full(self.shape, self._value, dtype=self.dtype)

    def _clone(self) -> Self:
        cloned = DeferredFullTensor(self.shape, self.dtype, self._value)
        cloned.requires_grad = self.requires_grad
        return cloned

    def _serialize(self, context):
        context.metadata["shape"] = tuple(self.shape)
        context.metadata["dtype"] = str(self.dtype)
        context.metadata["fill_value"] = self._value

    @staticmethod
    def deserialize(_, context):
        size = torch.Size(context.metadata["shape"])
        _, dtype = context.metadata["dtype"].split(".")
        dtype = getattr(torch, dtype)
        value = context.metadata["fill_value"]

        return DeferredFullTensor(size, dtype=dtype, value=value)


@register_serializer()
class DeferredGraphTensor(DeferredTensor):
    """A deferred tensor defined by a JIT Graph."""

    def __new__(
        cls,
        jit_graph: str,
        args: List[torch.Tensor],
        size: torch.Size,
        dtype: Optional[torch.dtype] = None,
    ):
        data = torch.empty(size, dtype=dtype, device="cpu")
        return cls._make_subclass(cls, data, require_grad=False)

    def __init__(
        self,
        jit_graph: str,
        args: List[torch.Tensor],
        size: torch.Size,
        dtype: Optional[torch.dtype] = None,
    ):
        """Constructs a `DeferredFullTensor` instance.

        Args:
            size: The size of the tensor.
            dtype: The data type of the tensor. If not specified, defaults to
                the default torch dtype.
            value: The value to fill the tensor with. If not specified, defaults
                to uninitialized data.
        """
        super().__init__()

        self._jit_graph = jit_graph
        self._args = args

    @property
    def jit_graph(self) -> str:
        return self._jit_graph

    def _to_cpu(self) -> torch.Tensor:
        try:
            output = cerebras_pytorch_lib.execute_jit_graph(
                self._jit_graph, self._args
            )
        except:
            logging.error(f"Failed to execute {self._jit_graph}")
            raise
        # This is a sanity check. We are unlikely to hit this case, but if we do, it's a bug.
        if len(output) != 1:
            raise ValueError(
                f"JIT graph must return a single tensor but got {len(output)}. "
                f"This is an internal bug. Please report to Cerebras."
            )
        result = output[0]

        if result.dtype != self.dtype:
            # Convert to the expected dtype.
            # This is needed due to a torchscript bug where the final cast is not properly traced.
            return result.to(self.dtype)
        return result

    def _clone(self) -> Self:
        cloned = DeferredGraphTensor(
            self._jit_graph,
            [
                a.clone() if isinstance(a, DeferredTensor) else a
                for a in self._args
            ],
            self.shape,
            self.dtype,
        )
        cloned.requires_grad = self.requires_grad
        return cloned

    def _serialize(self, context) -> None:
        context.metadata["jit_graph"] = self._jit_graph
        context.metadata["shape"] = tuple(self.shape)
        context.metadata["dtype"] = str(self.dtype)

        return {"args": list(map(context.serialize, self._args))}

    @staticmethod
    def deserialize(value, context) -> Self:
        jit_graph = context.metadata["jit_graph"]
        args = value["args"]

        shape = context.metadata["shape"]
        _, dtype = context.metadata["dtype"].split(".")
        dtype = getattr(torch, dtype)

        return DeferredGraphTensor(jit_graph, args, shape, dtype)


@register_serializer()
class DeferredSafeTensor(DeferredTensor):
    """A deferred tensor stored in a safetensor file."""

    @classmethod
    def open(cls, path, **kwargs):
        try:
            import safetensors
        except ImportError:
            logging.error(
                "Failed to import safetensors. Please install safetensors to "
                "load a safetensor file using cstorch.load"
            )
            raise

        kwargs.setdefault("framework", "pt")
        return safetensors.safe_open(path, **kwargs)

    @classmethod
    def load_file(cls, path):
        with cls.open(path) as f:
            return {k: cls(path, k, f) for k in f.keys()}

    def __new__(cls, path: str, key: str, fp=None):
        try:
            import safetensors.torch
        except ImportError:
            logging.error(
                "Failed to import safetensors. Please install safetensors to "
                "load a safetensor file using cstorch.load"
            )
            raise

        if fp is None:
            ctx = cls.open(path)
        else:
            ctx = nullcontext(fp)

        with ctx as f:
            slice = f.get_slice(key)
            shape = slice.get_shape()
            dtype = safetensors.torch._getdtype(slice.get_dtype())

        data = torch.empty(shape, dtype=dtype, device="cpu")
        return cls._make_subclass(cls, data, require_grad=False)

    def __init__(self, path: str, key: str, fp=None):
        """Constructs a `DeferredSafeTensor` instance.

        Args:
            path: Path to safetensor file
            key: Key at which the tensor is stored
            fp: Optional file pointer to the safetensor file
        """
        super().__init__()

        self._path = path
        self._key = key

    def _to_cpu(self) -> torch.Tensor:
        with self.open(self._path) as f:
            return f.get_tensor(self._key)

    def _clone(self) -> Self:
        cloned = DeferredSafeTensor(self._path, self._key)
        cloned.requires_grad = self.requires_grad
        return cloned

    def _serialize(self, context) -> None:
        context.metadata["path"] = self._path
        context.metadata["key"] = self._key

    @staticmethod
    def deserialize(value, context) -> Self:
        path = context.metadata["path"]
        key = context.metadata["key"]
        return DeferredSafeTensor(path, key)


@register_serializer()
class DeferredFileTensor(DeferredTensor):
    """A deferred tensor whose data is stored in a binary file."""

    def __new__(cls, filepath: str, size: torch.Size, dtype: torch.dtype):
        data = torch.empty(size, dtype=dtype, device="cpu")
        return cls._make_subclass(cls, data, require_grad=False)

    def __init__(self, filepath: str, size: torch.Size, dtype: torch.dtype):
        """Constructs a `DeferredFileTensor` instance.

        Args:
            filepath: The path to the binary file that holds the tensor data.
            size: The size of the tensor.
            dtype: The data type of the tensor.
        """
        super().__init__()

        self._filepath = Path(filepath).resolve()

        # Store the last stat of the file so we can check if the file
        # has been modified since the tensor was created before materializing it
        self._last_stats = self._filepath.stat()

    def _to_cpu(self) -> torch.Tensor:
        _check_file_modification(
            self._filepath.stat(),
            self._last_stats,
            f"materialize deferred tensor from file {self._filepath}",
        )

        # Return a read-only file-backed tensor. Upon write, the tensor will
        # be converted to an in-memory tensor.
        return torch.from_file(
            str(self._filepath),
            shared=False,  # Opens in read-only mode
            size=self.shape.numel(),
            dtype=self.dtype,
        ).reshape(self.shape)

    def _clone(self) -> Self:
        cloned = DeferredFileTensor(self._filepath, self.shape, self.dtype)
        cloned.requires_grad = self.requires_grad
        return cloned

    def _serialize(self, context) -> None:
        if not use_external_link or not self.shape:
            # When external links are disabled, we need to materialize the
            # tensor and save it to file. But note that we don't cache the
            # materialized tensor to avoid OOM.
            return context.serialize(self._materialize(cache_override=False))

        context.metadata["filepath"] = self._filepath
        context.metadata["shape"] = tuple(self.shape)
        context.metadata["dtype"] = str(self.dtype)

    @staticmethod
    def deserialize(value, context) -> Self:
        if value is not None:
            # If we saved a materialized tensor, then there is
            # nothing more to do here
            return value

        filepath = context.metadata["filepath"]
        size = torch.Size(context.metadata["shape"])
        _, dtype = context.metadata["dtype"].split(".")
        dtype = getattr(torch, dtype)

        return DeferredFileTensor(filepath=filepath, size=size, dtype=dtype)


def _check_file_modification(
    latest_stats: StorageReader.Stats,
    expected_stats: StorageReader.Stats,
    msg: str,
):
    """Check whether the backing file has been modified since the tensors was created."""
    if check_deferred_backing_storage and _timestamp_changed(
        latest_stats, expected_stats
    ):
        raise RuntimeError(
            f"Attempting to {msg}, but the file has "
            f"since been modified. The loaded tensor value may be "
            f"different from originally loaded tensor. Please refrain "
            f"from modifying the file while the run is in progress. "
            f"If this is a false positive, you can disable this check "
            f"by using the following context:"
            f"\n\tfrom cerebras.pytorch.saver.storage import check_deferred_backing_storage"
            f"\n\twith check_deferred_backing_storage(False):"
            f"\n\t\t... # Code that materializes the tensor\n"
        )


def _timestamp_changed(
    lhs: StorageReader.Stats, rhs: StorageReader.Stats
) -> bool:
    """Returns whether timestamp difference is above a certain threshold."""
    return abs(rhs.st_mtime - lhs.st_mtime) > 1
