# Configuration file for the Sphinx documentation builder.
import datetime
import os
import sys
import typing as t

# -- Project information

if t.TYPE_CHECKING:
    pass

from autoapi.mappers.python.objects import PythonPythonMapper
from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)))

# Project info

project = "Squirrel Datasets"
copyright = f"{datetime.datetime.now().year}, Merantix Momentum"
author = "Merantix Momentum"
# -- General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "autoapi.extension",
    "sphinxcontrib.mermaid",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "squirrel": ("https://squirrel-core.readthedocs.io/en/latest", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

autoclass_content = "both"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add logo and favicon
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"

# Document Python Code
autoapi_type = "python"
autoapi_dirs = ["../src/squirrel_datasets_core"]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autoapi_options = [
    "members",
    "undoc-members",
    # "private-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]


def skip_util_classes(
    app: Sphinx, what: str, name: str, obj: PythonPythonMapper, skip: bool, options: t.List[str]
) -> bool:
    """Called for each object to decide whether it should be skipped."""
    if what == "attribute" and name.endswith(".logger"):
        skip = True
    if name.startswith("squirrel.integration_test"):
        skip = True
    if name.startswith("test_"):
        skip = True
    return skip


def setup(sphinx: Sphinx) -> None:
    """Set up sphinx by registering custom skip function."""
    sphinx.connect("autoapi-skip-member", skip_util_classes)
