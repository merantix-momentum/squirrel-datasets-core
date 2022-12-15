import typing as t

import torch
import torchvision.transforms.functional as F
from squirrel_datasets_core.driver.huggingface import HuggingfaceDriver
from torch.utils.data import DataLoader
from torch.utils.data._utils.collate import default_collate 

BATCH_SIZE = 16


def hf_pre_proc(item: t.Dict[str, t.Any]) -> t.Dict[str, torch.Tensor]:
    """Converts the data coming from Huggingface to `torch.Tensor`s, such that the torch DataLoader
        can read it. We return only the `fine_label`s and not the `coarse_label`s of the CIFAR100
        dataset.

    Args:
        item (t.Dict[str, t.Any]): Sample coming from the Huggingface servers.

    Returns:
        t.Dict[str, torch.Tensor]: Ssample containing data as tensors.
    """
    return {
        "img": F.pil_to_tensor(item["img"]) / 255,
        "label": torch.tensor(item["fine_label"]),
    }


train_driver = (
    HuggingfaceDriver("cifar100")  # can be any of above drivers, just adapt hf_pre_proc
    .get_iter("train")
    .split_by_worker_pytorch()
    .map(hf_pre_proc)
    .batched(BATCH_SIZE, default_collate)
    .to_torch_iterable()
)
train_loader = DataLoader(train_driver, batch_size=None, num_workers=2)

# your train loop
for batch in train_loader:
    assert type(batch["img"]) == torch.Tensor
    assert len(batch["img"]) == BATCH_SIZE
    # forward pass ...
