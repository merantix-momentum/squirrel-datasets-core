import os
import typing as t
from collections import defaultdict

import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as tud
import torchvision.transforms as tr
from squirrel.catalog import Catalog
from squirrel.iterstream.torch_composables import SplitByRank, SplitByWorker, TorchIterable
from torch.nn.parallel import DistributedDataParallel as DDP

# check out the other tutorials if you are unfamiliar with the squirrel Catalog API
CATALOG = Catalog.from_plugins()


def collate(records: t.List[t.Dict[str, t.Any]]) -> t.Dict[str, t.List[torch.Tensor]]:
    """Specifies how to create a batch from a list of records.

    Args:
        records (t.List[t.Dict[str, t.Any]]): A list of records to package in a batch.

    Returns:
        t.Dict[str, t.List[torch.Tensor]]: The resulting batch.
    """

    batch = defaultdict(list)
    for elem in records:
        for k, v in elem.items():
            if isinstance(v, torch.Tensor):
                v = v.cpu().numpy().tolist()
            batch[k].append(v)
    out = {k: torch.from_numpy(np.asarray(v)) for k, v in batch.items()}
    return out


def augmentation_map(r: t.Dict[str, t.Any], augmentation: tr.Compose) -> t.Dict[str, t.Any]:
    """Applies augmentation to image.

    Args:
        r (t.Dict[str, t.Any]): A dict containing "image".
        augmentation (tr.Compose): Torch augmentation to use.

    Returns:
        t.Dict[str, t.Any]: A dict with an augmented image.
    """

    return {"image": augmentation(r["image"]), "label": r["label"]}


def get_dataloaders() -> t.Tuple[tud.DataLoader, tud.DataLoader]:
    """Constructs train and test dataloader objects for the MNIST train set.

    Returns:
        t.Tuple[tud.DataLoader, tud.DataLoader]: Train and test dataloader objects.
    """

    # convert data to Tensor, s.t. tud.DataLoader can handle it
    train_augment = tr.Compose([tr.ToTensor(), tr.Lambda(lambda x: (255 * x + torch.rand_like(x)) / 256 - 0.5)])
    test_augment = tr.Compose([tr.ToTensor(), tr.Lambda(lambda x: 255 * x / 256 - 0.5)])

    def train_augmentation_map(x: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return augmentation_map(x, train_augment)

    def test_augmentation_map(x: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return augmentation_map(x, test_augment)

    mnist_train = (
        CATALOG["mnist"]
        .get_driver()
        .get_iter("train")  # use squirrel API from previous tutorials up to this point
        .compose(SplitByRank)  # split data for each GPU
        .compose(SplitByWorker)  # split data for each process on each GPU
        .map(train_augmentation_map)  # run-time transformation (convert to torch.Tensor here)
        .take(10000)  # return only on the first 10000 samples (only to make demo faster)
        .batched(20, collation_fn=collate)  # create batches here, not in tud.DataLoader
        .compose(TorchIterable)  # make iterable compatible with tud.DataLoader
    )

    # same comments apply as for mnist_train
    mnist_test = (
        CATALOG["mnist"]
        .get_driver()
        .get_iter("test")
        .compose(SplitByRank)
        .compose(SplitByWorker)
        .map(test_augmentation_map)
        .take(1000)
        .batched(50, collation_fn=collate)
        .compose(TorchIterable)
    )

    # batch_size=None, because we already batched the data using squirrel
    train_loader = tud.DataLoader(mnist_train, num_workers=2, batch_size=None)
    test_loader = tud.DataLoader(mnist_test, num_workers=2, batch_size=None)

    return train_loader, test_loader


def evaluate(net: nn.Module, loader: tud.DataLoader, dev: torch.device) -> float:
    """Evaluate model performance given a dataloader.

    Args:
        net (nn.Module): Model to evaluate.
        loader (tud.DataLoader): Loader to load data from.
        dev (torch.device): Which device to push data to.

    Returns:
        float: Mean accuracy on all batches loaded from loader.
    """

    net.eval()
    with torch.no_grad():
        accs = []
        for batch in loader:
            b = batch["image"].float().to(dev)
            lbl = batch["label"].long().to(dev)
            pred = net(b.reshape(-1, 28**2))
            accs += (pred.argmax(-1) == lbl.flatten()).cpu().numpy().tolist()

    return float(np.mean(accs))


def run(rank: int) -> None:
    """Construct, train and test the model.

    Args:
        rank (int): Rank of the current process.
    """

    model = nn.Sequential(
        nn.Linear(28**2, 1024),
        nn.GELU(),
        nn.BatchNorm1d(1024),
        nn.Linear(1024, 1024),
        nn.GELU(),
        nn.BatchNorm1d(1024),
        nn.Linear(1024, 1024),
        nn.GELU(),
        nn.Linear(1024, 10),
    )

    torch.cuda.set_device(rank)
    dev = f"cuda:{rank}" if torch.cuda.is_available() else "cpu"
    model = model.to(dev)
    model = DDP(model, device_ids=[rank])

    xent = nn.CrossEntropyLoss()
    opter = optim.SGD(params=model.parameters(), lr=0.01, momentum=0.5)

    train_loader, test_loader = get_dataloaders()

    for idx, batch in enumerate(train_loader):
        if idx % 20 == 0:
            print(f"rank: {rank}, step: {idx:03d}, accuracy: {evaluate(model, test_loader, dev)}")
        b = batch["image"].float().to(dev)
        lbl = batch["label"].long().to(dev)

        model.train()
        opter.zero_grad()
        pred = model(b.reshape(-1, 28**2))
        loss = xent(pred, lbl)
        loss.backward()
        opter.step()

    print(f"rank: {rank}, step: {idx:03d}, accuracy: {evaluate(model, test_loader, dev)}")


def init_dist(rank: int) -> None:
    """Initialize distributed process group using the nccl backend.

    Args:
        rank (int): Rank of the current process.
    """
    world_size = torch.cuda.device_count()

    print(f"initing ... {rank}/{world_size}")
    dist.init_process_group("nccl", init_method="env://", rank=rank, world_size=world_size)
    print(f"done initing rank {rank}")


def main_worker(rank: int) -> None:
    """Initialize rank, set process start method to "spawn" and run training and eval routine.

    Args:
        rank (int): Rank of the current process.
    """
    if isinstance(rank, list):
        rank = rank[0]

    init_dist(rank)
    print(f"Rank {rank} initialized? {dist.is_initialized()}")

    run(rank)


if __name__ == "__main__":
    """
    INSTRUCTIONS: This tutorial showcases how to train a classifier using squirrel on multiple GPUs.
        The multiprocess spawning is taken care of by the PyTorch launch utilities. On the squirrel
        side, you just need to add `.compose(SplitByRank)` and `.compose(SplitByWorker)` to your iterable
        to train on multiple GPUs. Thereby your data is split by rank (i.e., your different GPUs)
        and by workers (i.e., the number of processes running on this rank). Don't forget to make your
        iterable a TorchIterable by calling `.compose(TorchIterable)`. Finally, simply pass your
        iterable to a torch DataLoader.

    SYSTEM: Code was tested on the following system:
        - OS: Ubuntu 20.04.3 LTS
        - NVIDIA-SMI 450.119.04, Driver Version: 450.119.04, CUDA Version: 11.0
        - Two Tesla T4 GPUs
        - torch 1.10.2+cu113, torchvision 0.11.3+cu113 installed with
            `pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113
            -f https://download.pytorch.org/whl/cu113/torch_stable.html`
        - squirrel-core==0.12.0, squirrel-datasets-core==0.0.1

    USAGE: To start the training process run the following command in the terminal
        `torchrun --nproc_per_node=GPU_COUNT 10.Distributed_MNIST.py` where GPU_COUNT is the
        number of GPUs you would like to use.
    """
    main_worker(int(os.environ["LOCAL_RANK"]))
