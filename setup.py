#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import itertools
import os
import re
import sys
from pathlib import Path

from setuptools import find_packages, setup

SOURCE_DIR = "src/squirrel_datasets_core"

# Read package information from other files so that just one version has to be maintained.
_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("./%s/__init__.py" % SOURCE_DIR, "rb") as f:
    init_contents = f.read().decode("utf-8")

    def get_var(var_name: str) -> str:
        """Parsing of squirrel_datasets_core project infos defined in __init__.py"""
        pattern = re.compile(r"%s\s+=\s+(.*)" % var_name)
        match = pattern.search(init_contents).group(1)
        return str(ast.literal_eval(match))

    version = get_var("__version__")


def assert_version(ver: str) -> None:
    """Assert version follows semantics such as 0.0.1 or 0.0.1-dev123. Notice English letters are not allowed after
    'dev'.
    """
    pattern = (
        r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
        + r"(?P<prepost>\.post\d+|(dev|a|b|rc)\d+)?(?P<devsuffix>[+-]dev)?\d*$"
    )
    assert bool(re.match(pattern, ver)), ValueError(
        f"Version string '{ver}' does not conform with regex '{pattern}', which is required by pypi metadata "
        "normalization."
    )


def normalize_version(_version: str, _version_tag: str) -> str:
    """Normalize version string according to tag build or dev build, to conform with the standard of PEP 440."""
    if "dev" in _version_tag:
        # remove alphabetic characters after keyword 'dev', which is forbidden PEP 440.
        short_sha = _version_tag[3:]  # substring after the word 'dev'
        numberic_sha = "".join([char for char in short_sha if char.isdigit()])
        _version += "-dev" + numberic_sha
    else:
        # In tag build, use the $TAG_NAME as the version string.
        _version = _version_tag.replace("v", "")
    assert_version(_version)
    return _version


# add tag to version if provided
if "--version_tag" in sys.argv:
    v_idx = sys.argv.index("--version_tag")
    version_tag = sys.argv[v_idx + 1]
    version = normalize_version(version, version_tag)
    sys.argv.remove("--version_tag")
    sys.argv.pop(v_idx)


def parse_req(spec: str) -> str:
    """Parse package name==version out of requirements file."""
    if ";" in spec:
        # remove restriction
        spec, _ = [x.strip() for x in spec.split(";", 1)]
    if "#" in spec:
        # remove comment
        spec = spec.strip().split("#")[0]
    if "\\" in spec:
        # remove line breaks
        spec = spec.strip().split("\\")[0]
    if "--hash=" in spec:
        # remove line breaks
        spec = spec.strip().split("--hash=")[0]
    return spec


if os.path.exists("requirements.in"):
    with open("requirements.in") as fh:
        requirements = [parse_req(r) for r in fh.read().replace("\\\n", " ").split("\n") if parse_req(r) != ""]
else:
    requirements = []

# generate extras based on requirements files
extras_require = dict()
for a_extra in ["dev", "preprocessing", "torchvision", "hub"]:
    req_file = f"requirements.{a_extra}.in"
    if os.path.exists(req_file):
        with open(req_file) as fh:
            extras_require[a_extra] = [r for r in fh.read().split("\n") if ";" not in r]
    else:
        extras_require[a_extra] = []
extras_require["all"] = list(itertools.chain.from_iterable(extras_require.values()))

if os.path.exists("scripts"):
    SCRIPTS = [os.path.join("scripts", a) for a in os.listdir("scripts")]
else:
    SCRIPTS = []

ENTRY_POINTS = {"squirrel": ["squirrel_datasets_core = squirrel_datasets_core.squirrel_plugin"]}

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# TODO remove after beta-testing phase
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.8",
    "Typing :: Typed",
]

# Setup package using PIP
if __name__ == "__main__":
    setup(
        name="squirrel_datasets_core",
        version=version,
        description="Squirrel public datasets collection",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Merantix Momentum",
        license="Apache 2.0",
        # Needed to make jinja work and not get linting errors in the rendered file
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        scripts=SCRIPTS,
        include_package_data=True,
        install_requires=requirements,
        tests_require=extras_require["dev"],
        extras_require=extras_require,
        entry_points=ENTRY_POINTS,
        classifiers=classifiers,
        package_data={"": ["*.rst"]},
    )
