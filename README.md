<div align="center">
  
# <img src="https://raw.githubusercontent.com/merantix-momentum/squirrel-datasets-core/main/docs/source/_static/logo.png" width="150px"> Squirrel Datasets Core
  
[![Python](https://img.shields.io/pypi/pyversions/squirrel-datasets-core.svg?style=plastic)](https://badge.fury.io/py/squirrel-datasets-core)
[![PyPI](https://badge.fury.io/py/squirrel-datasets-core.svg)](https://badge.fury.io/py/squirrel-datasets-core)
[![Conda](https://img.shields.io/conda/vn/conda-forge/squirrel-datasets-core)](https://anaconda.org/conda-forge/squirrel-datasets-core)
[![Documentation Status](https://readthedocs.org/projects/squirrel-datasets-core/badge/?version=latest)](https://squirrel-datasets-core.readthedocs.io)
[![Downloads](https://static.pepy.tech/personalized-badge/squirrel-datasets-core?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/squirrel-datasets-core)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://raw.githubusercontent.com/merantix-momentum/squirrel-datasets-core/main/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6420214.svg)](https://doi.org/10.5281/zenodo.6420214)
[![Generic badge](https://img.shields.io/badge/Website-Merantix%20Momentum-blue)](https://merantix-momentum.com)
[![Slack](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://join.slack.com/t/squirrel-core/shared_invite/zt-14k6sk6sw-zQPHfqAI8Xq5WYd~UqgNFw)

</div>

---
# What is Squirrel Datasets Core?

`squirrel-datasets-core` is an extension of the [Squirrel](https://github.com/merantix-momentum/squirrel-core) library. `squirrel-datasets-core` is a hub where the user can 1) explore existing datasets registered in the data mesh by other users and 2) preprocess their datasets and share them with other users. As an end user, you will
be able to load many publically available datasets with ease and speed with the help of `squirrel`, or load and preprocess
your own datasets with the tools we provide here. 

For preprocessing, we currently support Spark as the main tool to carry out the task.

If you have any questions or would like to contribute, join our [Slack community](https://join.slack.com/t/squirrel-core/shared_invite/zt-14k6sk6sw-zQPHfqAI8Xq5WYd~UqgNFw)!

# Installation
Install `squirrel-core` and `squirrel-datasets-core` with pip:

```shell
pip install squirrel-core[all]
pip install squirrel-datasets-core[all]
```
# Documentation

Visit our documentation on [Readthedocs](https://squirrel-datasets-core.readthedocs.io).

# Contributing
`squirrel-datasets-core` is open source and community contributions are welcome!

# The humans behind Squirrel
We are [Merantix Momentum](https://merantix-momentum.com/), a team of ~30 machine learning engineers, developing machine learning solutions for industry and research. Each project comes with its own challenges, data types and learnings, but one issue we always faced was scalable data loading, transforming and sharing. We were looking for a solution that would allow us to load the data in a fast and cost-efficient way, while keeping the flexibility to work with any possible dataset and integrate with any API. That's why we build Squirrel – and we hope you'll find it as useful as we do! By the way, [we are hiring](https://merantix-momentum.com/about#jobs)!


# Citation

If you use Squirrel Datasets in your research, please cite Squirrel using:
```bibtex
@article{2022squirrelcore,
  title={Squirrel: A Python library that enables ML teams to share, load, and transform data in a collaborative, flexible, and efficient way.},
  author={Squirrel Developer Team},
  journal={GitHub. Note: https://github.com/merantix-momentum/squirrel-core},
  year={2022}
}
```
