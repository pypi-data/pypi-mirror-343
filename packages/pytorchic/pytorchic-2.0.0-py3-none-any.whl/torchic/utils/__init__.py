import logging
import os
from typing import Optional

import torch

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("torchic")

DEVICE: str = "cpu"
if torch.accelerator.is_available() and os.environ.get("CI") != "true":
    current_accelerator: Optional[torch.device] = (
        torch.accelerator.current_accelerator()
    )
    if current_accelerator is not None:
        DEVICE = current_accelerator.type

logger.info(f"Using {DEVICE} device")
