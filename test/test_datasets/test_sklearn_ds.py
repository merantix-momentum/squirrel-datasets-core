from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from squirrel.catalog import Catalog

TAKE = 1


@pytest.mark.parametrize("cat_key", ["iris", "diabetes", "wine", "breast_cancer"])
def test_toy_data(plugin_catalog: Catalog, cat_key: str) -> None:
    """Test toydatasets which are internal to sklearn."""
    sample = plugin_catalog[cat_key].get_driver().get_iter().take(TAKE).collect()
    assert len(sample) > 0

@pytest.mark.skip(reason="Dataset is on public storage.")
@pytest.mark.parametrize("cat_key", ["california_housing", "olivetti_faces"])
def test_sklearn_data_downloading_exception(plugin_catalog: Catalog, cat_key: str) -> None:
    """Test that downloading data fails via if undesired."""
    with pytest.raises(Exception):
        plugin_catalog[cat_key].get_driver(download_if_missing=False).get_iter().take(TAKE).collect()

@pytest.mark.skip(reason="Dataset is on public storage.")
@pytest.mark.parametrize("cat_key", ["california_housing", "olivetti_faces"])
def test_california_housing_data_downloading(plugin_catalog: Catalog, cat_key: str) -> None:
    """Test that we can download data and yield from it"""
    with TemporaryDirectory as temp_dir:
        sample = plugin_catalog[cat_key].get_driver(data_home=temp_dir,
                                                    download_if_missing=True).get_iter().take(TAKE).join()
        assert len(sample) > 0
        assert len(list(Path(temp_dir).glob("*"))) > 0
