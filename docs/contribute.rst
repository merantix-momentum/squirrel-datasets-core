Contribute
====================

To contribute to developing this package, check out its Github repository and push commits there.

How do we handle pip requirements?
-------------------------------------

We mostly follow `this workflow <https://kennethreitz.org/essays/2016/02/25/a-better-pip-workflow>`_

#. Add packages to ``requirements.in``. Only pin versions that need to be pinned to make the code runnable. 
   Always specify the largest range of possible versions to ensure a maximum of compatibility with other packages.
#. Ask our devs to freeze your requirements into ``requirements.txt``. This is not allowed from external users for
   security reasons.
#. Commit ``requirements.in`` and ``requirements.txt`` in a PR. Once merged to main, Cloudbuild will build the
   image with the new dependencies.


Tests
-------------------------------------

You can run tests by executing ``pytest``. Prior make sure that you installed the testing extras i.e. via
``pip install -e .[dev]``.

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
