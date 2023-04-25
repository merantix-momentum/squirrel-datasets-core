from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from squirrel.catalog import Catalog

from squirrel_datasets_core.driver.sklearn import SklearnDriver, TOY_DATASETS

TAKE = 10

def test_get_dataset_names() -> None:
    names = SklearnDriver.get_dataset_names()
    assert len(names) > 0
    
@pytest.mark.parametrize("cat_key", TOY_DATASETS)
def test_stuff(plugin_catalog: Catalog, cat_key: str) -> None:
    stuff = plugin_catalog[f"{cat_key}_sklearn"].get_driver()._get_data()
    raise ValueError(stuff)
    
@pytest.mark.parametrize("cat_key", TOY_DATASETS)
def test_toy_data(plugin_catalog: Catalog, cat_key: str) -> None:
    """Test toydatasets which are internal to sklearn."""
    sample = plugin_catalog[f"{cat_key}_sklearn"].get_driver().get_iter().take(TAKE).collect()
    assert len(sample) > 0
    
@pytest.mark.skip(reason="Dataset is on public storage.")       
@pytest.mark.parametrize("cat_key", ["20newsgroups", "california_housing"])
def test_real_data(plugin_catalog: Catalog, cat_key: str) -> None:
    sample = plugin_catalog[f"{cat_key}_sklearn"].get_driver().get_iter().take(TAKE).collect()
    assert len(sample) > 0
    
@pytest.mark.skip(reason="Dataset is on public storage.")
@pytest.mark.parametrize("cat_key", ["olivetti_faces"])
def test_sklearn_data_downloading_exception(plugin_catalog: Catalog, cat_key: str) -> None:
    """Test that downloading data fails via if undesired."""
    with pytest.raises(Exception):
        plugin_catalog[cat_key].get_driver(download_if_missing=False).get_iter().take(TAKE).collect()

@pytest.mark.skip(reason="Dataset is on public storage.")
@pytest.mark.parametrize("cat_key", ["california_housing", "olivetti_faces"])
def test_california_housing_data_downloading(plugin_catalog: Catalog, cat_key: str) -> None:
    """Test that we can download data and yield from it"""
    with TemporaryDirectory() as temp_dir:
        sample = plugin_catalog[f"{cat_key}_sklearn"].get_driver(data_home=temp_dir,
                                                    download_if_missing=True).get_iter().take(TAKE).collect()
        assert len(sample) > 0
        assert len(list(Path(temp_dir).glob("*"))) > 0
        
