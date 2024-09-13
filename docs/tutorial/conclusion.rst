.. include:: ../colors.rst
.. include:: ../common.rst

Conclusion
==========

We can finally run our end-to-end test:

.. code:: console

    $ python -m pytest -sv docs/line_monitor/tests/e2e/test_line_monitor.py
    ==================================================================== test session starts =====================================================================
    platform linux -- Python 3.10.7, pytest-7.0.1, pluggy-1.0.0 -- /home/yoav/.cache/pypoetry/virtualenvs/testix-rvJpiJ6N-py3.10/bin/python
    cachedir: .pytest_cache
    hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/home/yoav/work/testix/.hypothesis/examples')
    rootdir: /home/yoav/work/testix
    plugins: asyncio-0.16.0, cov-3.0.0, hypothesis-6.37.0
    collected 1 item

    docs/line_monitor/tests/e2e/test_line_monitor.py::test_line_monitor PASSED

    ===================================================================== 1 passed in 0.08s ======================================================================



We have plenty of tests, and 100% code coverage.

.. code:: console

    docs/line_monitor/tests/unit/26/test_line_monitor.py::test_lauch_subprocess_with_pseudoterminal PASSED
    docs/line_monitor/tests/unit/26/test_line_monitor.py::test_receive_output_lines_via_callback PASSED
    docs/line_monitor/tests/unit/26/test_line_monitor.py::test_monitoring_with_no_callback PASSED
    docs/line_monitor/tests/unit/26/test_line_monitor.py::test_callback_registered_mid_monitoring PASSED
    docs/line_monitor/tests/unit/26/test_line_monitor.py::test_receive_output_lines_via_callback__process_ends__orderly_close PASSED

    ---------- coverage: platform linux, python 3.10.7-final-0 -----------
    Name                                          Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------------------
    docs/line_monitor/source/26/line_monitor.py      38      0   100%

Since we practiced Test Driven Development:

#. *Every single line* of our code is justified.
#. Every edge case we thought about is documented - via our tests. While tests written in Python are less readable than actual documentation written in English - they are much, much more reliable. If we have a good CI system to run our tests - this form of documentation does not get outdated.
#. Every bugfix that was performed was *first* reproduced with a test - and only *then* fixed in the code - *proving* that the bug is, in fact, fixed.
#. Our code is minimalist - we do not have unneeded code "just in case" which always ends up causing bugs.

But we should also mention the higher level benefits:

#. We coaxed the problem into an unambiguous, technically well-defined form - a bunch of tests.
#. Thus, we made sure that we understand the problem at hand.
#. Only then, did we proceed to try to solve it.
#. And when we did, we had the means to prove it.

Returning to the student analogy from ":ref:`importance_of_proper_failure`", we gave the student
a test to solve, instead of writing a test to fit the student's solution.

In one word - we were *logical* about it.

This is the proper way to write code. When done properly, it increases both
development speed and the quality of the product delivered.

Now you know.

**Use this knowledge. Write good code.**
