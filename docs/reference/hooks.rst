.. include:: ../colors.rst
.. include:: ../common.rst

Hooks
=====

|testix| allows us to simulate asynchronous events like this using its ``Hook`` construct.
Essentially ``Hook(function, *args, **kawrgs)`` can be injected into the middle of a ``Scenario``,
and it will call ``function(*args, **kwargs)`` at the point in which it's injected.

Here's how to write such a test. In this example, we have a ``LineProcessor`` class that reads lines from a stream.
If you register a callback with the ``LineProcessor``, it will call it every time it reads a line.

We want to simulate the situation where a callback is registered (from another
thread) in the middle of reading a stream, so we expect lines that are read
after the callback is registered to be passed on to it.

.. code:: python

    with Scenario() as s:
        s.input_stream.readline() >> 'line 1'
        s.input_stream.readline() >> 'line 2'
        s << Hook(tested.register_callback, Fake('my_callback')) 
        # the hook will execute right after the 'line 2' readline finishes
        # we therefore expect that after reading the next line, the callback will be called
        s.input_stream.readline() >> 'line 3'
        s.my_callback('line 3')
        s.input_stream.readline() >> 'line 4'
        s.my_callback('line 4')

        tested = LineProcessor(Fake('input_stream')) # no callbacks at this time
        tested.read_lines(Fake('input_stream'))
