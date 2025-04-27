import os
from dataclasses import dataclass

import deepspeed


@dataclass
class DSFunc:
    get_accelerator = deepspeed.accelerator.real_accelerator.get_accelerator
    is_current_accelerator_supported = (
        deepspeed.accelerator.real_accelerator.is_current_accelerator_supported
    )


def is_current_accelerator_supported():
    return (
        get_accelerator().device_name() == "vacc"
        or DSFunc.is_current_accelerator_supported()
    )


ds_accelerator = None


def get_accelerator():
    from deepspeed.accelerator.real_accelerator import (  # pylint:disable=import-outside-toplevel
        _validate_accelerator,
        accel_logger,
    )

    global ds_accelerator  # pylint:disable=global-statement
    if ds_accelerator is not None:
        return ds_accelerator

    accelerator_name = None
    ds_set_method = None
    if "DS_ACCELERATOR" in os.environ:
        accelerator_name = os.environ["DS_ACCELERATOR"]
        if accelerator_name == "vacc":
            try:
                import torch_vacc  # pylint:disable=import-outside-toplevel
            except ImportError as e:
                raise ValueError(
                    "VACC_Accelerator requires torch_vacc, which is not installed on this system."
                ) from e
        else:
            return DSFunc.get_accelerator()
        ds_set_method = "override"
    if accelerator_name is None:
        try:
            import torch_vacc  # pylint:disable=import-outside-toplevel

            accelerator_name = "vacc"
        except ImportError:
            accelerator_name = None
        ds_set_method = "auto detect"

    if accelerator_name == "vacc":
        from .vacc_accelerator import (  # pylint:disable=import-outside-toplevel
            VACC_Accelerator,
        )

        ds_accelerator = VACC_Accelerator()
    else:
        return DSFunc.get_accelerator()
    _validate_accelerator(ds_accelerator)
    if accel_logger is not None:
        accel_logger.info(
            "Setting ds_accelerator to %s (%s)",
            ds_accelerator._name,  # pylint:disable=protected-access
            ds_set_method,
        )
    return ds_accelerator
