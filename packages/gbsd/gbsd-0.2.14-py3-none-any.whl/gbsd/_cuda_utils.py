from functools import cache
from typing import Generator

import torch


@cache
def get_device_count():
    import nvidia_smi
    nvidia_smi.nvmlInit()

    return nvidia_smi.nvmlDeviceGetCount()
    

def split_chunk(tensor: torch.Tensor) -> Generator[tuple[str, torch.Tensor], None, None]:
    device_count = get_device_count()

    for device_idx, chunk in enumerate(torch.chunk(tensor, device_count)):
        device = f"cuda:{device_idx}"
        chunk = chunk.to(device)

        yield device, chunk
