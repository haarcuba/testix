.. include:: ../../colors.rst
.. include:: ../../common.rst

Line Monitor Unit Tests
=======================

We now turn to developing, TDD style, our :doc:`LineMonitor <../design>` library.

Developing Test Driven style means we add behaviours one by one, for each behaviour we
go through the |RED|-|GREEN|-|REFACTOR| loop:

#. |RED|: write a :doc:`properly failing test <../fail_properly>`
#. |GREEN|: write code that passes the test - the code doesn't have to be pretty
#. |REFACTOR|: tidy up the code to make it readable

Sometimes the |REFACTOR| step is not needed, but we should always at least consider it.

Let's go.

.. toctree::
   :maxdepth: 1

   launching_the_subprocess
   monitoring_the_output
   recap_1
   watching_the_subprocess
