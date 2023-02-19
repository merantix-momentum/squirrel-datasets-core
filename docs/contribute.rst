Contribute
====================

To contribute to developing this package, check out its Github repository and push commits there.

How do we handle dependencies?
-------------------------------------

We use poetry for resolving and installing dependencies:

#. `Install poetry <https://python-poetry.org/docs/#installation>`_
#. Install the dependencies: ``poetry install --all-extras``. Poetry creates a virtual environment for you.
#. Add packages manually to ``pyproject.toml`` and run ``poetry lock --no-update`` or use ``poetry add [my-package]``.
#. ``requirements.txt`` will be updated via a pre-commit hook.
#. Commit ``poetry.lock`` and ``requirements.txt`` in a PR. Once merged to main, Cloudbuild will build the
   image with the new dependencies.


Tests
-------------------------------------

You can run tests by executing ``poetry run pytest``.

Build the documentation locally
-------------------------------------

Running ``poetry run sphinx-build ./docs ./docs/build`` from the root directory will generate the documentation.
Currently, this only works on python3.9.
You can use poetry with python3.9 by running ``poetry env use 3.9`` before ``poetry install --all-extras``.


Python Code Style Guide
--------------------------

We use PEP8 with some modifications.
We use `pre-commit <https://pre-commit.com>`_ to automatically check most of these points.
Visit `their website <https://pre-commit.com/#install>`_ to find out how to setup pre-commit for this repository and check your contributions before opening a PR.

* Code formatting should follow black with a 120 character line length. (checked and fixed by pre-commit)
* Using type-hints is mandatory.
  The only exception are the arguments ``self``, ``cls``, ``*args`` and ``*kwargs``. (checked for by pre-commit)
* Use `Google-style docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html/>`_ .
  This is mandatory for functions. Docstrings on classes and modules are optional.
  One line docstrings for simple functions are okay. (checked for by pre-commit)
* Don't do `from X import *`. It hinders code readability.
* String formatting (e.g. string concatenation/composition) is done via f-strings.
* Avoid cyclical imports. To avoid cyclical imports when type hinting,
  follow `this <https://stackoverflow.com/a/39757388>`_ advice using the ``__future__`` approach.
