.. include:: ../../colors.rst
.. include:: ../../common.rst

Watching The Subprocess
=======================

If you try working with our current ``LineMonitor`` implementation
you will find it has some disadvantages.

#. There is no way to stop monitoring.
#. In particular, if the underlying subprocess crashes, the monitor will just
   block forever - it is blocked trying to ``.readline()`` - but the line will
   never come.

Furthermore, we originally wanted the ability to have more than one callback.

Let's improve our ``LineMonitor``, starting by handling the underlying subprocess a little more carefully.
We'll start by checking for available data before we try to read it.

Polling the Read File Descriptor
--------------------------------

We want to create a `polling object <https://docs.python.org/3/library/select.html#polling-objects>`_, and
register the reader's file descriptor using its `.register` method.

Let's test for it. We have to mock the `select` module, of course, and also change our `launch_scenario()`.

.. literalinclude:: ../../line_monitor/tests/unit/11/test_line_monitor.py
   :linenos:
   :lines: 6-20
   :emphasize-lines: 6-7,12-14

There is a quick here - after running ``patch_module(line_monitor, 'select')``, the ``select`` object
inside the tested ``line_monitor`` module is replace by a ``Fake('select')`` fake object. Later,
we want to demand that ``poller.register()`` be called with the ``select.POLLIN`` constant. As
things are, this would technically also be the fake object
``Fake('select.POLLIN')``, since |testix| automatically generates fake objects
whenever you lookup a ``Fake``'s attribute (unless it's explicitly set up).

While it is possible to demand


.. code:: python

   s.poller.register('reader_descriptor', Fake('select').POLLIN)

And it will work just fine, I find it less readable. Therefore I'd rather "rescue" the ``POLLIN``
object from the real ``select`` and assign it to the fake ``select``.

You may notice another quirk - the function ``.fileno()`` returns a file descriptor, which
is an integer. However, in our test we make it return a string value, ``'reader_descriptor'``,
and later test that this value is transmitted to the ``.register()`` call on the polling object.

Of course it is possible to write something like

.. code:: python

    FAKE_FILE_DESCRIPTOR = 12121212
    s.reader.fileno() >> FAKE_FILE_DESCRIPTOR
    s.poller.register(FAKE_FILE_DESCRIPTOR, select.POLLIN)

This is totally legitimate. However, In my opinion, when testing the logic of
"this object from *here* should get *there*",
using strings (which are immutable in Python) may be more readable than using
the correct data type.

Changing ``launch_scenario`` has changed our tests, let's run them, see if they fail:

.. code:: console

    $ python -m pytest -sv docs/line_monitor/tests/unit/11/test_line_monitor.py

    ...

    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: select.poll()
    E        actual  : subprocess.Popen(['my', 'command', 'line'], stdout = 'write_to_fd', close_fds = True)

Yay :) we have |RED|. Our tests expect the new ``.poll()`` logic, but our code, of course, is still not up to date.
Of course, all of our tests now fail, since they all depend on ``launch_scenario()`` being followed exactly.

Let's get to |GREEN| with this and then continue with testing the actual polling:


.. literalinclude:: ../../line_monitor/source/12/line_monitor.py
   :linenos:
   :emphasize-lines: 3,17-18

Now our tests pass once again. We have |GREEN|, but we haven't really added the actual
feature we want to develop. We want the monitor to stop monitoring once the underlying
subprocess is dead, and not get blocked trying to read a line that will never come.

This will involve using the poll object to poll the read descriptor to see
that there's some data to read before calling `.readline()`. Since our tests
already involve various scenarios calling `.readline()` - doing this TDD
doesn't mean writing new tests - it means modifying the tests that we have.

This happens sometimes in TDD, and it's perfectly normal. Now, let's get to |RED|.

Looking at an excerpt from our tests:

.. code:: python

    with Scenario() as s:
        launch_scenario(s)
        tested.launch_subprocess(['my', 'command', 'line'])

        s.reader.readline() >> 'line 1'
        s.my_callback('line 1')
        s.reader.readline() >> 'line 2'
        s.my_callback('line 2')
        s.reader.readline() >> 'line 3'
        s.my_callback('line 3')


We want to demand that every ``.readline()`` is preceded by a ``.poll()``, and
to only be performed if there's input available. The ``.poll()`` call returns a
list of ``[(file_descriptor, events), ...]`` pairs, where events is a bitmask
of flags indicating the state of the file descriptor (e.g. ``POLLIN | POLLOUT``).

Still, the sequence of ``.poll()`` and ``.readline()`` is sort-of "the new readline",
it makes up a logical scenario, so let's write it as a scenario function, ``read_line_scenario``.

Here is our ``test_receive_output_lines_via_callback``, adapted to the new situation.

.. literalinclude:: ../../line_monitor/tests/unit/13/test_line_monitor.py
   :linenos:
   :lines: 27-34,35-51
   :emphasize-lines: 2-4,9-11,15,17,19,21


.. code:: console

    running this, we get |RED|

    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: poller.poll()
    E        actual  : reader.readline()


Very good. Now let's fix our code to pass the tests. Note that we did not yet add a test for
the case where the file descriptor does not have any data to read - that come later. Always
proceed in small, baby steps - and you'll be fine. Try to do it all at once, and you'll crash and burn.

Getting to |GREEN| is super easy, we add just this one line of code:

.. literalinclude:: ../../line_monitor/source/14/line_monitor.py
   :linenos:
   :lines: 21-27
   :emphasize-lines: 3


Well, this is |GREEN|, but adds little value. It's time for a serious test
that makes sure that ``.readline()`` is called *if and only if* ``POLLIN`` is present.
Let's get to |RED|.

We introduce a ``skip_line_scenario()``, and introduce it into our existing
tests, such that they represent the situation when sometimes there is no data to
read.

.. literalinclude:: ../../line_monitor/tests/unit/15/test_line_monitor.py
   :linenos:
   :emphasize-lines: 32-33,50-51,68,70,83

The idea here is simple - sometimes ``.poll()`` returns a result where the ``POLLIN`` flag is not set - and then we should skip the ``.readline()``.

Do we have |RED|? Yes we do:

.. code:: console

    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: poller.poll()
    E        actual  : reader.readline()

Let's get to |GREEN|. This requires us to add the following to our code:

.. literalinclude:: ../../line_monitor/source/16/line_monitor.py
   :linenos:
   :lines: 21-30
   :emphasize-lines: 3-6

This is |GREEN| but not the best code, the ``.monitor()`` function is becoming `too long <https://github.com/PracticeFoxyCode/practice#short-files-short-functions>`_, time for the |REFACTOR| step in
our |RED|-|GREEN|-|REFACTOR| loop.

.. literalinclude:: ../../line_monitor/source/17/line_monitor.py
   :linenos:
   :lines: 21-33
   :emphasize-lines: 3-4,10-13

Ah, much nicer.

Solving the Blocking Problem
----------------------------

We are now in a position not to block forever when data does not arrive.
To do that, we need to add a timeout on the ``.poll`` call - since as it
is now, it may still block forever waiting for some event on the file.

Getting to |RED| is simple in principle, e.g. if we want a 10 seconds timeout,
just change demands of our various scenarios, e.g.

.. code:: python

    def read_line_scenario(s, line):
        s.poller.poll(10) >> [('reader_descriptor', select.POLLIN)]
        # note the 10 second timeout above
        s.reader.readline() >> line

    # similarly for other poll scenario functions

If we do this, however - and later on discover that a 60 second timeout is more reasonable,
we will have to Test Drive the change from 10 to 60. This seems more annoying that it is helpful.
Sometimes, tests can be *too* specific.

|testix| has a way to specifically ignore the values of specific arguments -
you specify the special value ``IgnoreArgument()`` instead of the overly
specific ``10``.

Here's how to use it in this case:

.. literalinclude:: ../../line_monitor/tests/unit/18/test_line_monitor.py
   :linenos:
   :lines: 28-36
   :emphasize-lines: 2,6,9

Using this we get to |RED|

.. code:: console

    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: poller.poll(|IGNORED|)
    E        actual  : poller.poll()

Note the ``|IGNORED|`` annotation. Getting to green is now a matter of adding this timeout
in our code:

.. literalinclude:: ../../line_monitor/source/19/line_monitor.py
   :linenos:
   :lines: 30-33
   :emphasize-lines: 2

And we have |GREEN| again.

Oops, a bug
~~~~~~~~~~~

If you try this code, you will find that there's a bug: in real life `.poll()` may return an empty list.

When we find a bug, the TDD way is of course to write a test that reproduces it, and then fix the code.
In our case, let's add a ``poll_returns_empty_scenario`` and sprinkle it in our existing tests,
thus covering the behaviour with and without a callback, etc.

.. literalinclude:: ../../line_monitor/tests/unit/20/test_line_monitor.py
   :linenos:
   :lines: 35-36,41-62
   :emphasize-lines: 17

This gets us into |RED| territory

.. code:: console

    E       IndexError: list index out of range

Now let's fix the bug.

.. literalinclude:: ../../line_monitor/source/21/line_monitor.py
   :linenos:
   :lines: 30-35
   :emphasize-lines: 3-4

We are now |GREEN|, and, since we are working TDD, we have a test for this bug - *and it will not return in the future*.

Has the Subprocess Died?
------------------------

We are now ready to add functionality to stop the monitor in case the subprocess itself has died.
We will want our code to use ``.poll()`` on the ``Popen`` object itself,
and if ``.poll()`` returns a non-None value, stop the monitor.

If you think about it, we can poll the subprocess only when there's
no data available. It may be that there is data to read and process has died,
but in that case, we'll just discover it is dead when the data runs out. This
way we make sure we read all the data out of the pipe when the process has died,
even if it takes more than one read.

If, however, there's no data to read, *and* the process is dead - then there's no point
in continuing to monitor the pipe for more data, and we should close the reader, e.g.

.. literalinclude:: ../../line_monitor/tests/unit/22/test_line_monitor.py
   :linenos:
   :lines: 38-40,44-68
   :emphasize-lines: 17,19,21

Note that we demand process polling only after no data was ready to read,
here it only comes after some ``skip_line*scenario`` function.

This brings us into |RED| territory. Current we have not taken the case that the process dies into account,
but as usual, we're taking things slowly. Let's get to |GREEN|.

.. literalinclude:: ../../line_monitor/source/23/line_monitor.py
   :linenos:
   :lines: 12-29
   :emphasize-lines: 8,13

Note that this is the first time we bothered to save the subprocess ``Popen`` object!
This is another example of how TDD helps us. If the test passes without us making some move - then
we simply don't make it. This helps us write minimalistic code. Remember, code
that doesn't exist - has no bugs.

We are now in |GREEN| - so let's get into |RED| again, and add a specific test for the "process has died scenario":

.. literalinclude:: ../../line_monitor/tests/unit/24/test_line_monitor.py
   :linenos:
   :lines: 41-44, 116-134
   :emphasize-lines: 1-3,20

Note that we no longer need the ``TestixLoopBreaker`` trick - since we now expect the ``.monitor()`` function
to simply finish and break out of its infinite loop.

Are we in |RED|? Yes we are:

.. code:: console

    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: reader.close()
    E        actual  : poller.poll(10)

The test wants the infinite loop to finish and close the reader, but the code just goes on.

Let's fix our code:

.. literalinclude:: ../../line_monitor/source/25/line_monitor.py
   :linenos:
   :lines: 21-32
   :emphasize-lines: 4-7

We're |GREEN|, but this function has grown too long again, so let's |REFACTOR|.

.. literalinclude:: ../../line_monitor/source/26/line_monitor.py
   :linenos:
   :lines: 21-39
   :emphasize-lines: 4-7,13-15,17-18

Not shorter, but more semantically clear, at least it my opinion. Since we have
tests, we can refactor without fear - since we can always make sure we
are still in the |GREEN|!
