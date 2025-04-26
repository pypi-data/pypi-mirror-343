# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from qai_hub_models.models.hrnet_pose import MODEL_ID, App, Model  # noqa: F401
from qai_hub_models.utils.quantization import (
    Precision,
    quantized_folder_deprecation_warning,
)

quantized_folder_deprecation_warning(
    "hrnet_pose_quantized", "hrnet_pose", Precision.w8a8
)
