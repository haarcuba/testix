.. include:: ../colors.rst
.. include:: ../common.rst

Design of the LineMonitor
=========================

Python has an excellent library called `subprocess <https://docs.python.org/3/library/subprocess.html>`_, which allows a quite generic inteface for launching subprocsses using its `Popen` class.

We want to have a ``LineMonitor`` class which:

#. will launch subprocesses using |subprocess| under the hood
#. will allow the caller to register callbacks that get called from every line of output from the subprocess
#. will also implement an iterator form, e.g. you can write something like

    .. code:: python

       for line in line_monitor:
            print(f'this just in: {line}')


Since this is a Test Driven Development tutorial as well as a |testix| tutorial, let's discuss the tests.

First a short primer on types of tests.

.. _unit_tests:

Unit Tests
----------

Unit tests check that each unit of code (usually a single class or module) performs the correct business logic.

Generally speaking, unit tests

#. test logic
#. do not perform I/O (perhaps only to local files)
#. use mocks (not always, but many times) - this is where |testix| comes in.

Integration Tests
-----------------

Integration tests test that various "units" fit together.

Generally speaking, integration tests

#. perform some actual I/O
#. do not rigorously test logic (that's the unit test's job)


End-to-End (E2E) Tests
----------------------

In our case, since the project is quite small,
the integration test will actually test the scope of the entire project.
and so it is more appropriately called an End-to-End (E2E) Test.

In real projects, E2E tests usually include

#. an actual deployment, which is as similar as possible to real life deployments.
#. various UI testing techniques, e.g. launching a web-browser to use some webapp

In our toy example, we don't have such complications.

Let's move on.
