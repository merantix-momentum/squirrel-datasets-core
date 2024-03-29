import pytest
from squirrel.catalog import Catalog

TAKE = 1


@pytest.mark.skip(reason="Dataset is on public storage.")
def test_caltech_public_data(plugin_catalog: Catalog) -> None:
    """Test loading Caltech101 via torchvision."""
    try:
        plugin_catalog["caltech"].get_driver().get_iter().take(TAKE).join()
    except RuntimeError as e:
        if str(e).startswith("The daily quota of the file 101_ObjectCategories.tar.gz is exceeded"):
            pytest.skip(msg=f"Failed to download data due to quota limit. original error: {str(e)}")
        else:
            raise e


@pytest.mark.parametrize("cifar_set", ["cifar10", "cifar100"])
@pytest.mark.parametrize("split", ["train", "test"])
@pytest.mark.skip(reason="Dataset is on public storage.")
def test_cifar_public_data(plugin_catalog: Catalog, cifar_set: str, split: str) -> None:
    """Test loading CIFAR-10 via torchvision."""
    # version==2 is torchvision
    version = 2
    # torchvision.dataset.CIFAR10 and CIFAR100 use `train: bool` instead of `split: str`
    plugin_catalog[cifar_set][version].get_driver().get_iter(train=(split == "train")).take(TAKE).join()


@pytest.mark.parametrize("split", ["byclass", "bymerge", "balanced", "letters", "digits", "mnist"])
@pytest.mark.skip(reason="Dataset is on public storage.")
def test_emnist_public_data(plugin_catalog: Catalog, split: str) -> None:
    """Test loading EMNIST via torchvision."""
    plugin_catalog["emnist"].get_driver().get_iter(split=split).take(TAKE).join()
