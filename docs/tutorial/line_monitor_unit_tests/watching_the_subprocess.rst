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

Let's get to |GREEN|.
