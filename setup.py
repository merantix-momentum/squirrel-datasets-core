#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import itertools
import os
import re
import sys

from setuptools import setup

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

# add tag to version if provided
if "--version_tag" in sys.argv:
    v_idx = sys.argv.index("--version_tag")
    version = version + "." + sys.argv[v_idx + 1]
    sys.argv.remove("--version_tag")
    sys.argv.pop(v_idx)

if os.path.exists("README.rst"):
    with open("README.rst") as fh:
        readme = fh.read()
else:
    readme = ""
if os.path.exists("HISTORY.md"):
    with open("HISTORY.md") as fh:
        history = fh.read().replace(".. :changelog:", "")
else:
    history = ""


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

# Setup package using PIP
if __name__ == "__main__":
    setup(
        name="squirrel_datasets_core",
        version=version,
        python_requires=">=3.8.0",
        description="Squirrel public datasets collection",
        long_description=f"{readme}\n\n{history}",
        author="Merantix Labs GmbH",
        license="",
        # Needed to make jinja work and not get linting errors in the rendered file
        package_dir={"": "src"},
        packages=["squirrel_datasets_core"],
        scripts=SCRIPTS,
        include_package_data=True,
        install_requires=requirements,
        tests_require=extras_require["dev"],
        extras_require=extras_require,
        entry_points=ENTRY_POINTS,
        classifiers=["Public"],
        package_data={"": ["*.rst"]},
    )
