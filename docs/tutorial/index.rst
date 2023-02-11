.. include:: ../colors.rst
.. include:: ../common.rst

Tutorial
========

This tutorial will walk you through `Test Driven Development <https://en.wikipedia.org/wiki/Test-driven_development>`_ using |testix| and pytest_.

.. _pytest: https://docs.pytest.org/en/latest/

We will develop a small project in this tutorial, test driven of course, which
solves the following real-life problem: suppose you want to run some subprocess,
and you want to read its output line-by-line in real time and take appropriate action.

An example application might be that you want to monitor live logs and do something
whenever a log line has :code:`ERROR` in it.

Let's call this library :code:`LineMonitor`.

.. toctree::
    design
    e2e_test
    fail_properly
    basics/index.rst
    line_monitor_unit_tests/index.rst
    conclusion.rst
    more_about_readability.rst


