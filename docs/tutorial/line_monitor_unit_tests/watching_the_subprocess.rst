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
things are, this would technically also be the fake objcet
``Fake('select.POLLIN')``, since |testix| automatically generates fake objects
whenever you lookup a ``Fake``'s attribute (unless it's explicitly set up).

While it is possible to demand


.. code:: python

   s.poller.register('reader_descriptor', Fake('select').POLLIN)

and it will work just fine, I find it less readable. Therefore I'd rather "rescue" the ``POLLIN`` 
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

yay :) we have |RED|. Our tests expect the new ``.poll()`` logic, but our code, of course, is still not up to date.
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


we want to demand that every ``.readline()`` is preceeded by a ``.poll()``, and
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

Do we have |RED|? yes we do:

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

Ahh, much nicer.

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

using this we get to |RED|

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
