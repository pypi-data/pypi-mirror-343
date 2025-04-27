# ==============================================================================
#
# Copyright (C) 2025 VastaiTech Technologies Inc.  All rights reserved.
#
# ==============================================================================
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author :        wyl
@Email :   algorithm@vastaitech.com
@Time  :     2025/02/18 16:17:38
'''

import torch
from .utils import VAPatchesManager, check_package_version


class DeepSpeedPatchManager(VAPatchesManager):
    """DeepSpeed Patch Manager"""
    patches_info = {}

    @classmethod
    def check_env(cls):
        return check_package_version("deepspeed", "0.16.3", "eq")

    @classmethod
    def patch_accelerator(cls):
        from .deepspeed.accelerator.real_accelerator import (
            get_accelerator, is_current_accelerator_supported)

        # from .deepspeed.accelerator.vacc_accelerator import VACC_Accelerator
        # NOTE(lance.0307): need test
        # import deepspeed
        # deepspeed.accelerator.real_accelerator.set_accelerator(VACC_Accelerator())
        cls.register_patch('deepspeed.accelerator.real_accelerator.get_accelerator', get_accelerator)
        cls.register_patch('deepspeed.accelerator.real_accelerator.is_current_accelerator_supported', is_current_accelerator_supported)

    @classmethod
    def patch_ops(cls):
        # NOTE(lance): deepspeed.ops.adam.FusedAdam has other params adam_w_mode & set_grad_none compare to torch.optim.Adam
        cls.register_patch('deepspeed.ops.adam.FusedAdam', torch.optim.AdamW)



    @classmethod
    def exec_adaptor(cls):
        if cls.check_env():
            from deepspeed.utils import logger
            logger.warning("DeepSpeed is detected, applying patches for vacc ...")
            cls.patch_accelerator()
            cls.patch_ops()
            cls.apply_patches()


DeepSpeedPatchManager.exec_adaptor()
