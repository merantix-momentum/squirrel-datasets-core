Merantix Labs - Squirrel Datasets Core
================================================================================
[![Python](https://img.shields.io/pypi/pyversions/squirrel-datasets-core.svg?style=plastic)](https://badge.fury.io/py/squirrel-core)
[![PyPI](https://badge.fury.io/py/squirrel-datasets-core.svg)](https://badge.fury.io/py/squirrel-core)
[![Downloads](https://pepy.tech/badge/squirrel-datasets-core)](https://pepy.tech/project/squirrel-core)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Documentation Status](https://readthedocs.org/projects/squirrel-datasets-core/badge/?version=latest)](https://docs.squirrel.merantixlabs.cloud/)
[![Generic badge](https://img.shields.io/badge/Website-Merantix%20Momentum-blue.svg)](https://www.merantixlabs.com/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/squirrel-core/shared_invite/zt-14k6sk6sw-zQPHfqAI8Xq5WYd~UqgNFw)

# What is Squirrel Datasets Core?

`squirrel-datasets-core` is a hub where the user can 1) explore existing datasets registered in the data mesh by other users and 2) preprocess their datasets and share them with other users. As an end user, you will
be able to load many publically available datasets with ease and speed with the help of `squirrel`, or load and preprocess
your own datasets with the tools we provide here. 

For preprocessing, we currently support Spark as the main tool to carry out the task.

Please see our [documentation](https://squirrel-datasets-core.readthedocs.io) for further details.

If you have any questions or would like to contribute, join our Slack community!

# Installation
Squirrel Datasets Core requires the latest stable version of Squirrel Core to be installed:

```shell
pip install squirrel-core
```

Install Squirrel Datasets Core via:

```shell
pip install squirrel-datasets-core
```

# Contributing
Squirrel is open source and community contributions are welcome!

Check out the [contribution guide](https://docs.squirrel.merantixlabs.cloud/usage/contribute.html) to learn how to get involved.

# The humans behind Squirrel
We are [Merantix Momentum](https://merantixlabs.com/), a team of ~30 machine learning engineers, developing machine learning solutions for industry and research. Each project comes with its own challenges, data types and learnings, but one issue we always faced was scalable data loading, transforming and sharing. We were looking for a solution that would allow us to load the data in a fast and cost-efficient way, while keeping the flexibility to work with any possible dataset and integrate with any API. That's why we build Squirrel – and we hope you'll find it as useful as we do! By the way, [we are hiring](https://www.merantixlabs.com/career)!


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