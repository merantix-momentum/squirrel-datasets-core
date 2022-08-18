from typing import Tuple

import pytest
from squirrel.catalog import Catalog

from squirrel_datasets_core.driver.huggingface import HuggingfaceDriver

TAKE = 10


@pytest.mark.skip(reason="Dataset is on public storage.")
def test_mnist_public_data(plugin_catalog: Catalog) -> None:
    """Test loading MNIST hosted by Hugging Face"""
    driver: HuggingfaceDriver = plugin_catalog["mnist"].get_driver()
    data = driver.get_iter(split="train").take(TAKE).collect()
    assert len(data) == TAKE


@pytest.mark.parametrize("cifar_set", ["cifar10", "cifar100"])
@pytest.mark.parametrize("split", ["train", "test"])
@pytest.mark.skip(reason="Dataset is on public storage.")
def test_cifar_public_data(plugin_catalog: Catalog, cifar_set: str, split: str) -> None:
    """Test loading CIFAR10 hosted by Hugging Face."""
    # version==1 is huggingface
    driver: HuggingfaceDriver = plugin_catalog[(cifar_set, 1)].get_driver()
    data = driver.get_iter(split=split).take(TAKE).collect()
    assert len(data) == TAKE


@pytest.mark.parametrize(
    "catalog_key", [("wikitext-103-raw", 1), ("wikitext-103", 1), ("wikitext-2-raw", 1), ("wikitext-2", 1)]
)
@pytest.mark.parametrize("split", ["train", "test"])
@pytest.mark.skip(reason="Dataset is on public storage.")
def test_wikitext_public_data(plugin_catalog: Catalog, catalog_key: Tuple[str, int], split: str) -> None:
    """Test loading wikitext datasets hosted by Hugging Face."""
    driver: HuggingfaceDriver = plugin_catalog[catalog_key].get_driver()
    data = driver.get_iter(split=split).take(TAKE).collect()
    assert len(data) == TAKE
