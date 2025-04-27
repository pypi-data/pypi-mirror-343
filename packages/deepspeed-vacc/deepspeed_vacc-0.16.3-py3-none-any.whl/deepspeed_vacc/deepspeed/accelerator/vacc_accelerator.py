import os
import pkgutil
import importlib

from deepspeed.accelerator.abstract_accelerator import DeepSpeedAccelerator

# During setup stage torch may not be installed, pass on no torch will
# allow op builder related API to be executed.
try:
    import torch_vacc
    import torch.vacc
except ImportError as e:
    raise ImportError(
        "VACC_Accelerator requires torch_vacc, which is not installed on this system."
    ) from e


class VACC_Accelerator(DeepSpeedAccelerator):
    def __init__(self):  # pylint: disable=super-init-not-called
        self._name = "vacc"
        self._communication_backend_name = "vccl"
        self._compile_backend = "inductor"

    def is_synchronized_device(self):
        # TODO(qingsong): change to False after async stream is merged
        return False

    def use_host_timers(self):
        return self.is_synchronized_device()

    def resolves_data_dependency(self):
        return self.is_synchronized_device()

    def handles_memory_backpressure(self):
        return self.is_synchronized_device()

    # Device APIs
    def device_name(self, device_index=None):
        if device_index is None:
            return "vacc"
        return f"vacc:{device_index}"

    def device(self, device_index=None):
        return torch.vacc.device(device_index)

    def set_device(self, device_index):
        torch.vacc.set_device(device_index)

    def current_device(self):
        return torch.vacc.current_device()

    def current_device_name(self):
        return f"vacc:{torch.vacc.current_device()}"

    def device_count(self):
        return torch.vacc.device_count()

    def synchronize(self, device_index=None):
        return torch.vacc.synchronize(device_index)

    # RNG APIs
    def random(self):
        return torch.random

    def set_rng_state(self, new_state, device_index=None):
        if device_index is None:
            return torch.vacc.set_rng_state(new_state)

        return torch.vacc.set_rng_state(new_state, device_index)

    def get_rng_state(self, device_index=None):
        if device_index is None:
            return torch.vacc.get_rng_state()

        return torch.vacc.get_rng_state(device_index)

    def manual_seed(self, seed):
        return torch.vacc.manual_seed(seed)

    def manual_seed_all(self, seed):
        return torch.vacc.manual_seed_all(seed)

    def initial_seed(self, seed):
        return torch.vacc.initial_seed(seed)

    def default_generator(self, device_index):
        return torch.vacc.default_generators[device_index]

    # Streams/Events
    @property
    def Stream(self):
        return torch.vacc.Stream

    def stream(self, stream):
        return torch.vacc.stream(stream)

    def current_stream(self, device_index=None):
        return torch.vacc.current_stream(device_index)

    def default_stream(self, device_index=None):
        return torch.vacc.default_stream(device_index)

    @property
    def Event(self):
        return torch.vacc.Event

    def available_memory(self, device_index=None):
        return torch.vacc.get_device_properties(device_index).total_memory

    # Memory management
    def empty_cache(self):
        return torch.vacc.empty_cache()

    def memory_allocated(self, device_index=None):
        return torch.vacc.memory_allocated(device_index)

    def max_memory_allocated(self, device_index=None):
        return torch.vacc.max_memory_allocated(device_index)

    def reset_max_memory_allocated(self, device_index=None):
        return torch.vacc.reset_max_memory_allocated(device_index)

    def memory_cached(self, device_index=None):
        return torch.vacc.memory_cached(device_index)

    def max_memory_cached(self, device_index=None):
        return torch.vacc.max_memory_cached(device_index)

    def reset_max_memory_cached(self, device_index=None):
        return torch.vacc.reset_max_memory_cached(device_index)

    def memory_stats(self, device_index=None):
        if hasattr(torch.vacc, "memory_stats"):
            return torch.vacc.memory_stats(device_index)

    def reset_peak_memory_stats(self, device_index=None):
        if hasattr(torch.vacc, "reset_peak_memory_stats"):
            return torch.vacc.reset_peak_memory_stats(device_index)

    def memory_reserved(self, device_index=None):
        if hasattr(torch.vacc, "memory_reserved"):
            return torch.vacc.memory_reserved(device_index)

    def max_memory_reserved(self, device_index=None):
        if hasattr(torch.vacc, "max_memory_reserved"):
            return torch.vacc.max_memory_reserved(device_index)

    def total_memory(self, device_index=None):
        return torch.vacc.get_device_properties(device_index).total_memory

    # Data types
    def is_bf16_supported(self):
        return torch.vacc.is_bf16_supported()

    def is_fp16_supported(self):
        return True

    def supported_dtypes(self):
        return [torch.float, torch.half]  # , torch.bfloat16]

    # Misc
    def amp(self):
        if hasattr(torch.vacc, "amp"):
            return torch.vacc.amp
        return None

    def is_available(self):
        return torch.vacc.is_available()

    def range_push(self, msg):
        if hasattr(torch.vacc, "nvtx") and hasattr(torch.vacc.nvtx, "range_push"):
            return torch.vacc.nvtx.range_push(msg)

    def range_pop(self):
        if hasattr(torch.vacc, "nvtx") and hasattr(torch.vacc.nvtx, "range_pop"):
            return torch.vacc.nvtx.range_pop()

    def lazy_call(self, callback):
        return torch.vacc._lazy_call(callback)  # pylint: disable=protected-access

    def communication_backend_name(self):
        return self._communication_backend_name

    def is_triton_supported(self):
        return False

    # Graph operations
    def create_graph(self):
        return None

    def capture_to_graph(self, graph, pool=None, stream=None):
        from deepspeed.runtime.utils import noop_context

        return noop_context()

    def replay_graph(self, graph):
        return

    # Tensor operations

    @property
    def BFloat16Tensor(self):
        return torch.vacc.BFloat16Tensor

    @property
    def ByteTensor(self):
        return torch.vacc.ByteTensor

    @property
    def DoubleTensor(self):
        return torch.vacc.DoubleTensor

    @property
    def FloatTensor(self):
        return torch.vacc.FloatTensor

    @property
    def HalfTensor(self):
        return torch.vacc.HalfTensor

    @property
    def IntTensor(self):
        return torch.vacc.IntTensor

    @property
    def LongTensor(self):
        return torch.vacc.LongTensor

    def pin_memory(self, tensor, align_bytes=1):
        return tensor
        # HACK(lance): pin_memory need torch > 2.3.0
        # return tensor.pin_memory()

    def is_pinned(self, tensor):
        return tensor.is_pinned()

    def on_accelerator(self, tensor):
        device_str = str(tensor.device)
        if device_str.startswith("vacc:"):
            return True
        else:
            return False

    def op_builder_dir(self):
        try:
            # is op_builder from deepspeed or a 3p version? this should only succeed if it's deepspeed
            # if successful this also means we're doing a local install and not JIT compile path
            from op_builder import __deepspeed__  # noqa: F401 # type: ignore

            return "op_builder"
        except ImportError:
            return "deepspeed.ops.op_builder"

    # dict that holds class name <--> class type mapping i.e.
    # 'AsyncIOBuilder': <class 'op_builder.async_io.AsyncIOBuilder'>
    # this dict will be filled at init stage
    class_dict = None

    def _lazy_init_class_dict(self):
        if self.class_dict is not None:
            return
        else:
            self.class_dict = {}
            # begin initialize for create_op_builder()
            # put all valid class name <--> class type mapping into class_dict
            op_builder_dir = self.op_builder_dir()
            op_builder_module = importlib.import_module(op_builder_dir)
            op_builder_absolute_path = os.path.dirname(op_builder_module.__file__)
            for _, module_name, _ in pkgutil.iter_modules([op_builder_absolute_path]):
                # avoid self references,
                # skip sub_directories which contains ops for other backend(cpu, npu, etc.).
                if (
                    module_name != "all_ops"
                    and module_name != "builder"
                    and not os.path.isdir(
                        os.path.join(op_builder_absolute_path, module_name)
                    )
                ):
                    module = importlib.import_module(
                        "{}.{}".format(op_builder_dir, module_name)
                    )
                    for member_name in module.__dir__():
                        if (
                            member_name.endswith("Builder")
                            and member_name != "OpBuilder"
                            and member_name != "CUDAOpBuilder"
                            and member_name != "TorchCPUOpBuilder"
                        ):  # avoid abstract classes
                            if not member_name in self.class_dict:
                                self.class_dict[member_name] = getattr(
                                    module, member_name
                                )
            # end initialize for create_op_builder()

    # create an instance of op builder and return, name specified by class_name
    def create_op_builder(self, class_name):
        self._lazy_init_class_dict()
        if class_name in self.class_dict:
            return self.class_dict[class_name]()
        else:
            return None

    # return an op builder class, name specified by class_name
    def get_op_builder(self, class_name):
        self._lazy_init_class_dict()
        if class_name in self.class_dict:
            return self.class_dict[class_name]
        else:
            return None

    def build_extension(self):
        from torch.utils.cpp_extension import BuildExtension # pylint:disable=import-outside-toplevel

        return BuildExtension

    def export_envs(self):
        return ["VCCL", "LD_LIBRARY", "PATH"]

    def visible_devices_envs(self):
        return ["VACC_VISIBLE_DEVICES"]

    def set_visible_devices_envs(self, current_env, local_accelerator_ids):
        for env in self.visible_devices_envs():
            current_env[env] = ",".join(map(str, local_accelerator_ids))

    def get_compile_backend(self):
        return self._compile_backend

    def set_compile_backend(self, backend):
        supported_backends = (
            torch._dynamo.list_backends(  # pylint: disable=protected-access
                exclude_tags=()
            )
        )
        if backend in supported_backends:
            self._compile_backend = backend
        else:
            raise ValueError(
                f"{backend} not supported by {self.device_name()}. Supported Backends are {supported_backends }"
            )
