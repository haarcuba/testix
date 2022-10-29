.. include:: ../../colors.rst
.. include:: ../../common.rst

Recap
=====

Let's recap a bit on what we've been doing in this tutorial.

We started with a test for the basic subprocess-launch behaviour, got to |RED|, implemented the code, and got to |GREEN|.

Next, when moving to implement the actual output monitoring behaviour, we kept the first test, 
and added a new one. This is very important in TDD - the old test keeps the old behaviour intact -
if, when implementing the new behaviour we break the old one - we will know.

When working with |testix|, you are encourage to track all your mocks (``Fake`` objects) very 
precisely. This effectively made us refactor the launch-process test scenario into a ``launch_scenario()``
helper function, since you must launch a subprocess before monitoring it. 

We also saw that adding a call to ``open`` made the original launch-process
test fail as well as the new monitor test. This makes sense, since the launching behaviour
now includes a call to ``open`` that it didn't before - and the code doesn't support that yet,
so the test fails.

Another thing we ran into is that sometimes we get |GREEN| even when we wanted |RED|.
This should make you uneasy - it usually means that the test is not really testing what
you think it is. In our case, however, it was just because an edge case which we 
added a test for was already covered by our existing code. When that happens,
strict TDD isn't really possible - and you need to revert to making sure
that if you break the code on purpose, it breaks the test in the proper manner.

YAGNI
-----

Another thing to notice, is that the call to ``Popen`` is simply

.. code:: python

    subprocess.Popen(*popen_args, **popen_kwargs)

And not, for example,

.. code:: python

    self._process = subprocess.Popen(*popen_args, **popen_kwargs)

Why didn't we save the subprocess in an instance variable?
Working TDD makes us want to get to |GREEN| - no more, no less. Since
we don't need to store the subprocess to pass the test, we don't do it.

Let me repeat that for you: **if we don't need it to pass the test, we don't do it**. 


You might say "but we need to hold on to the subprocess to control it, see if it's still alive, or kill it".

Well, maybe we do. If that's what we really think, we should express this need in a test - make sure it's |RED|, and
then write the code to make it |GREEN|. 

This is one particular way of implementing the `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it>`_ principle - if
you're not familiar with it, you should take the time to read about it.

Upholding the YAGNI requires a special kind of discipline, and TDD and |testix| in particular, helps us achieve it.

Code Recap
----------

Before we continue, here is the current state of our unit test  and
code.

The test:

.. literalinclude:: ../../line_monitor/tests/unit/7/test_line_monitor.py
   :linenos:

and the code that passes it

.. literalinclude:: ../../line_monitor/source/7/line_monitor.py
   :linenos:
