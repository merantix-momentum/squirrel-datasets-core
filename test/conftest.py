"""This module defines specific fixtures for unit tests. Shared fixtures are defined in shared_fixtures.py.

###################################
Please do not import from this file.
###################################

Not importing from conftest is a best practice described in the note here:
https://pytest.org/en/6.2.x/writing_plugins.html#conftest-py-local-per-directory-plugins
"""

import pytest
from squirrel.catalog import Catalog


@pytest.fixture()
def unit_test_fixture() -> str:
    """Fixture that is only used in the unit test scope."""
    return "unit test string"

@pytest.fixture()
def plugin_catalog() -> Catalog:
    """Create catalog from plugins."""
    return Catalog.from_plugins()
