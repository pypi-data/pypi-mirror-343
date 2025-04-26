# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from PIL.Image import Image


## Helper routines
def show_image(image: Image, masks: np.ndarray | None = None) -> None:
    """Show input image with mask applied"""
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    if masks is not None:
        _show_mask(masks, plt.gca())
    plt.axis("off")
    plt.savefig("demo_output.jpg", bbox_inches="tight")
    plt.show()


def _show_mask(mask: np.ndarray, ax: plt.Axes) -> None:
    """Helper routine to add mask over existing plot"""
    color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
