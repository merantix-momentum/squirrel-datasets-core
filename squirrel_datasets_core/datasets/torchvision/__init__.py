# Exemplary sources for the torchvision driver

from squirrel.catalog import Source, CatalogKey

__all__ = ["SOURCES"]

SOURCES = [
    (
        CatalogKey("caltech", 1),
        Source(driver_name="torchvision", driver_kwargs={"name": "Caltech101", "download": True}),
    ),
    (
        CatalogKey("cifar10", 2),
        Source(driver_name="torchvision", driver_kwargs={"name": "CIFAR10", "download": True}),
    ),
    (
        CatalogKey("cifar100", 2),
        Source(driver_name="torchvision", driver_kwargs={"name": "CIFAR100", "download": True}),
    ),
    (
        CatalogKey("emnist", 1),
        Source(driver_name="torchvision", driver_kwargs={"name": "EMNIST", "download": True}),
    ),
]
