.. include:: ../common.rst


Failing Properly
================

For convenience, here again is our :ref:`e2etest`:

.. literalinclude:: ../line_monitor/tests/e2e/test_line_monitor.py
   :linenos:
   :caption: end-to-end (E2E) test

If we run it will of course not work:

.. code-block:: console

   $ python -m pytest docs/line_monitor/tests/e2e

Results ultimately in

.. code-block:: console

    E   ModuleNotFoundError: No module named 'line_monitor'

That is because none of the code for ``line_monitor`` exits yet. This is a sort of failure, but it's not very interesting. 

What we want is for the test to fail *properly* - we want it to fail *not* because our system doesn't exist - we want it to fail because our system does not implement the correct behaviour yet. 

In concrete terms, we want it to fail because a subprocess has seemingly been launched, but its output has not been captured by our monitor. In short, we want it to fail on our
``assert`` statements, not due to some technicalities

So, let's write some basic code that achieves just that.  We create a ``line_monitor.py`` file 
within our ``import`` path with skeleton code:

.. _skeleton_line_monitor:

.. literalinclude:: ../line_monitor/source/0/line_monitor.py
   :linenos:
   :caption: line_monitor.py


Now if we run the test:

.. code-block:: console

   $ python -m pytest docs/line_monitor/tests/e2e


We get a proper failure

.. code-block:: console

    ....... OUTPUT SKIPPED FOR BREVITY .......

    >       assert captured_lines == EXPECTED_LINES
    E       AssertionError: assert [] == ['line 0', 'l...'line 5', ...]


This is a **proper failure** - the test has done everything right, but the current ``LineMonitor`` implementation does not deliver on its promises.


The Importance of Proper Failure
--------------------------------

Congratulations, we have a **failing test**! This is the first milestone when
developing a feature using Test Driven Development. Let's briefly explain whey
this is so important, and why this is superior to writing tests for previously
written, already working code.

Essentially, imagine we wrote a test, wrote some skeleton code, ran the test -
and it *didn't fail*. Well, that would obviously mean that our test was bad.
This is admittedly rare, but I've seen it happen.

The more common scenario however is that we wrote the test, wrote the skeleton
code, ran the test - and it failed, but *not in the way we planned*. This means
that the test does not, in fact, test what we want. 

If we write our test *after* we've developed our code, how will we ever know
that the test actually tests what we think it is testing? You'd be amazed at
the number of tests which exist out there and in fact, do not test what they
are supposed to.

I have seen with my own eyes, many times, tests that do not test *anything
at all*. This happens because once code has been written, the tests are written
to accommodate the code, which is *exactly* the opposite of what should happen.

The last point is super important so I will rephrase it in a more compelling
way: think about testing the performance of a human being, not a computer
program, e.g. testing a student in high school or university. Should we have
the student write his or her answers first, and *then* write the test to
accommodate these answers? *Utterly absurd*.

We should write the test first, and then use it to test the student.

If we write our tests first, and **fail them properly**,

* we make sure they actually test what they pretend to to
* we think hard about how to test this functionality - we gain focus on what our software is supposed to do
* we take pains to actually think about how the code will be use: we let the test drive the design of the application

So, it is essential before developing some behaviour, that our tests fail properly.

Now, let's get on with implementing the ``LineMonitor``. This will require - surprise - some more tests - unit tests, which is what |testix| is all about.
