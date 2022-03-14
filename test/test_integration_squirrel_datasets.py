import pytest
from squirrel.catalog import Catalog


@pytest.fixture()
def plugin_catalog() -> Catalog:
    """Create catalog from plugins."""
    return Catalog.from_plugins()


def test_squirrel_integration() -> None:
    """Test creation of catalog."""
    assert len(Catalog.from_plugins()) > 0


def test_mnist(plugin_catalog: Catalog) -> None:
    """Test loading mnist from hugging face."""
    plugin_catalog["mnist"].get_driver().get_iter("train").take(1).join()


# Marked as a flaky test to auto-retry
@pytest.mark.flaky(max_runs=4, min_passes=1)
@pytest.mark.serial
@pytest.mark.parametrize("cifar_set", ["cifar10", "cifar100"])
@pytest.mark.parametrize("split", ["train", "test"])
def test_cifar(plugin_catalog: Catalog, cifar_set: str, split: str) -> None:
    """Test Torch dataset cifar10 from hugging face."""
    plugin_catalog[cifar_set][1].get_driver().get_iter(split=split).take(1).join()
