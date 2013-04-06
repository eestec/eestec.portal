.. _conventions:

===========
Conventions
===========

Line length
===========

All Python code in this package should be PEP8 valid. However, we don't strictly
enforce the 80-char line length rule. It is encouraged to have your code
formatted in 80-char lines, but somewhere it's just more readable to break this
rule for a few characters. Long and descriptive test method names are a good
example of this.

.. note::
    Configuring your editor to display a line at 80th column helps a lot
    here and saves time.

.. note::
    The line length rules also applies to non-python source files, such as
    documentation .rst files.

About imports
=============

1. Don't use * to import `everything` from a module.
2. Don't use commas to import multiple stuff on a single line.
3. Don't use relative paths.

.. sourcecode:: python

    from collective.table.local import add_row
    from collective.table.local import delete_rows
    from collective.table.local import update_cell

instead of

.. sourcecode:: python

    from collective.table.local import *
    from collective.table.local import add_row, delete_rows
    from .local import update_cell


Sort imports
============

As another imports stylistic guide: Imports of code from other modules should
always be alphabetically sorted with no empty lines between imports. The only
exception to this rule is to keep one empty line between a group of
``from x import y`` and a group of ``import y`` imports.

.. sourcecode:: python

    from collective.table.tests.base import TableIntegrationTestCase
    from plone.app.testing import login

    import os

instead of

.. sourcecode:: python

    import os

    from plone.app.testing import login
    from collective.table.tests.base import TableIntegrationTestCase


Commit checklist
================

Before every commit you should:

* Run :ref:`unit-tests`.
* Run :ref:`syntax-validation`.
* Add an entry to :ref:`changelog` (if applicable).
* Add/modify :ref:`sphinx-docs` (if applicable).

.. note::
    All syntax checks and all tests can be run with a single command:

    .. sourcecode:: bash

        $ make tests

.. _unit-tests:

Unit tests
==========

Un-tested code is broken code.

For every feature you add to the codebase you must also add tests for it. Also
write a test for every bug you fix to ensure it doesn't crop up again in the
future.

You run tests like this:

.. sourcecode:: bash

    $ bin/test

To speed things up, you can choose to run only some tests, not all at once.
Use the ``-t`` to filter out tests and run only those that match the expression.

.. sourcecode:: bash

    # run only setup tests
    $ bin/test -t test_setup


.. _syntax-validation:

Syntax validation
=================

All Python source code should be `PEP-8` valid and checked for syntax errors.
The tools used for this are `flake8` and `zptlint`.

To validate your source code, run the following commands:

.. sourcecode:: bash

    $ bin/flake8 src/eestec/portal
    $ for pt in `find src/eestec/portal/ -name "*.pt"` ; do bin/zptlint $pt; done

    # or just this one (also runs all unit tests)
    # make tests


.. note::
    It pays off to invest a little time to make your editor run `flake8` on a
    file every time you save that file. Saves lots of time in the long run.


.. _changelog:

Changelog
=========

Feature-level changes to code are tracked inside ``docs/HISTORY.txt``. Examples:

- added feature X
- removed Y
- fixed bug Z

Add an entry every time you add/remove a feature, fix a bug, etc.

.. _sphinx-docs:

Sphinx Documentation
====================

Un-documented code is broken code.

For every feature you add to the codebase you should also add documentation
for it to ``docs/``.

After adding/modifying documentation, re-build `Sphinx` and check how it is
displayed:

.. sourcecode:: bash

    $ make docs
    $ open docs/html/index.html

Documentation is automatically generated from these source files every time
you push your code to GitHub. The post-commit hook is handled by ReadTheDocs and
the results are visible at http://eestecportal.readthedocs.org/.

.. _travis:

Travis Continuous Integration
=============================

On every push to GitHub, `Travis <http://travis-ci.org/eestec/eestec.portal>`_
runs all tests/syntax validation checks and reports failures (if there
are any) to ``it@eestec.net`` mailinglist and to the ``#ngep`` IRC channel.

Travis is configured with the ``.travis.yml`` file located in the root of
``eestec.portal`` package.

.. _git_workflow:

Git workflow & branching model
==============================

We only have one Python package for the entire portal, ``eestec.portal``,
version controled by Git on https://github.com/eestec/eestec.portal.

Git repository has the following layout:

* **feature branches**: all development for new features must be done in
  dedicated branches, normaly one branch per feature,
* **master branch**: when features get completed they are merged into the master
  branch; bugfixes are commited directly on the master branch,
* **tags**: whenever we deploy code to production we tag the repository so we
  can later re-trace our steps and revert broken deployments if necessary.

Hooks:

* On every change to the ``master`` branch, our :ref:`staging_env` gets
  re-deployed.
* On every new tag, our :ref:`production_env` gets re-deployed.


