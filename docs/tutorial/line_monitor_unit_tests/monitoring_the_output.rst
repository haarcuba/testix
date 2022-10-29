.. include:: ../../colors.rst
.. include:: ../../common.rst

Monitoring The Output
=====================

Next we want to test the following behaviour: we
register a callback with our ``LineMonitor`` object using its ``.register_callback()`` method,
and it calls our callback with each line of output 
it reads from the |pseudoterminal|.

Python streams have a useful ``.readline()`` method, so let's wrap the read file-descriptor of the |pseudoterminal| with a stream. It turns out
that you can wrap a file descriptor with a simple call to the built-on ``open()`` function, so we'll use that.


Note that we *add a new test*, leaving the previous one intact. This means that we *keep everything we already have working*, while we add a test for this new behaviour.

Let's start by describing a scenario where we read several lines from the
|pseudoterminal| and demand that they are transferred to our callback.

.. literalinclude:: ../../line_monitor/tests/unit/3/test_line_monitor.py
   :linenos:
   :lines: 18-32
   :emphasize-lines: 5,8-11,13-15

What's going on here?

* We add a demand that our code create a Python stream from the |pseudoterminal|'s read-descriptor before launching the subprocess.
* We then call `.launch_subprocess()` to meet those demands.
* We describe the "read-from-|pseudoterminal|-forwared-to-callback" data flow for 3 consecutive lines.
* We register a ``Fake('my_callback')`` object as our callback - this way, when the code calls the callback,
  it will be meeting our demands in this test. It's important that ``'my_callback'`` is used as this ``Fake``'s name,
  since we refer to it in the ``Scenario``.
* We then call the ``.monitor()`` method - this method should do all the reading and forwarding.

We must also remember to mock the built-in `open`:

.. literalinclude:: ../../line_monitor/tests/unit/3/test_line_monitor.py
   :linenos:
   :lines: 5-9
   :emphasize-lines: 5

We can already see a problem: the scenario is actually built out of two parts - 
the part which tests ``.launch_subprocess()``, and the part which tests ``.monitor()``.

Furthermore, since we have our previous test in ``test_lauch_subprocess_with_pseudoterminal``, which doesn't expect the call to ``open()``,
the two tests are in contradiction.

The way to handle this is to refactor our test a bit:

.. literalinclude:: ../../line_monitor/tests/unit/4/test_line_monitor.py
   :linenos:
   :emphasize-lines: 9,11-14,19,25


By convention, helper functions that help us modify scenarios end with `_scenario`.

OK this seems reasonable, let's get some |RED|! Running this both our tests fail:

.. code-block:: console

    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: open('read_from_fd', encoding = 'latin-1')
    E        actual  : subprocess.Popen(['my', 'command', 'line'], stdout = 'write_to_fd', close_fds = True)

We changed our expectations from ``.launch_subprocess()`` to call ``open()``, but we did not change the implementation yet, so |testix| is surprised to find that we actually call ``subprocess.Popen`` - and makes our test fail. 

Good, let's fix it and get to |GREEN|. We introduce the following to our code:

.. literalinclude:: ../../line_monitor/source/5/line_monitor.py
   :linenos:
   :emphasize-lines: 5-6,9,15,19-21

This passes the test, but that's not really what we meant - right? Obviously we
would like a ``while True`` to replace the `for _ in range(3)` here.

However, if we write a ``while True``, then |testix| will fail us for the 4th call to ``.readline()``,
since it only expects 3 calls.

Testing infinite, ``while True`` loops is a problem, but we can get around it
by injecting an exception that will terminate the loop. Just as we can determine what
calls to ``Fake`` objects return, we can make them raise exceptions.

|testix| even comes with an exception class just for this use case, ``TestixLoopBreaker`.`
Let's introduce another ``.readline()`` expectation into our test, using |testix|'s ``Throwing`` construct:

.. literalinclude:: ../../line_monitor/tests/unit/6/test_line_monitor.py
   :linenos:
   :lines: 22-38
   :emphasize-lines: 13,16-17

NOTE - we once more *change the test first*. Also note that we can use
``Throwing`` to raise any type of exception we want, not just ``TestixLoopBreaker``.

This gets us back into the |RED|.

.. code-block:: console

   E           Failed: DID NOT RAISE <class 'testix.TestixLoopBreaker'>

Since our code calls ``.readline()`` 3 times exactly, the fourth call,
which would have resulted in ``TestixLoopBreaker`` being raised, did not happen.

Let's fix our code:

.. literalinclude:: ../../line_monitor/source/7/line_monitor.py
   :linenos:
   :lines: 18-21
   :emphasize-lines: 2

And we're back in |GREEN|.

Edge Case Test: When There is no Callback
-----------------------------------------

What happens if ``.monitor()`` is called, but no callback
has been registered? We can of course implement all kinds of behaviour,
for example, we can make it "illegal", and raise an Exception from ``.monitor()``
in such a case.

However, let's do something else. Let's just define things such that output
collected from the subprocess when no callback has been registered is discarded.


.. literalinclude:: ../../line_monitor/tests/unit/8/test_line_monitor.py
   :linenos:
   :lines: 40-52


Notice there's no ``.register_callback()`` here. We demand that ``.readline()`` be called, but we don't demand anything else.

Running this fails with a |RED|

.. code-block:: console

        def monitor(self):
            while True:
                line = self._reader.readline()
    >           self._callback(line)
    E           TypeError: 'NoneType' object is not callable


Which reveals that we in fact, did not handle this edge case very well.

Let's add code that fixes this.

.. literalinclude:: ../../line_monitor/source/9/line_monitor.py
   :linenos:
   :lines: 18-23
   :emphasize-lines: 4-5

Our test passes - back to |GREEN|.
