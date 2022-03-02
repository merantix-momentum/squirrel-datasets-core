# Exemplary sources for the huggingface driver

from squirrel.catalog import Source, CatalogKey

__all__ = ["SOURCES"]

SOURCES = [
    (
        CatalogKey("mnist", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/mnist"},
            driver_kwargs={"name": "mnist"},
        ),
    ),
    (
        CatalogKey("cifar100", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/cifar100"},
            driver_kwargs={"name": "cifar100"},
        ),
    ),
    (
        CatalogKey("cifar10", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/cifar10"},
            driver_kwargs={"name": "cifar10"},
        ),
    ),
    (
        CatalogKey("wikitext-103-raw", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/wikitext"},
            driver_kwargs={"name": "wikitext", "subset": "wikitext-103-raw-v1"},
        ),
    ),
    (
        CatalogKey("wikitext-2-raw", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/wikitext"},
            driver_kwargs={"name": "wikitext", "subset": "wikitext-2-raw-v1"},
        ),
    ),
    (
        CatalogKey("wikitext-103", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/wikitext"},
            driver_kwargs={"name": "wikitext", "subset": "wikitext-103-v1"},
        ),
    ),
    (
        CatalogKey("wikitext-2", 1),
        Source(
            driver_name="huggingface",
            metadata={"src": "https://huggingface.co/datasets/wikitext"},
            driver_kwargs={"name": "wikitext", "subset": "wikitext-2-v1"},
        ),
    ),
]
