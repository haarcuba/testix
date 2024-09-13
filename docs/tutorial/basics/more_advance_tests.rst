.. include:: ../../colors.rst
.. include:: ../../common.rst

More Advanced Tests
===================

Specifying Return Values
------------------------

:doc:`Previously <working_with_scenarios_and_fake_objects>` we have specified
how a ``Fake`` object named ``"sock"`` should be used by our code.

When we say ``s.sock.send(b'the data')`` we express the expectation that the code
under test will call the ``.send()`` method with exactly one argument, whose value
should equal exactly ``b'the data'``.

When the code does this with ``"sock"``'s ``.send()`` method, however, what value
is returned by method call?

The answer in this case is ``None`` - but |testix| also allows us to define
this return value. This is useful when you want to test thing related to what
function calls on ``Fake`` objects return, e.g. thing about testing
some code that receives data on one socket, and sends the length of said data
to another socket.

We therefore expect that there will be a ``.recv()`` call on one socket which
returns some data, this data in turn is converted to a number (its length),
which is then encoded and sent on the outgoing socket.

Here's how to test this in |testix|

.. literalinclude:: other_tests/more_advanced/1/test_forward_lengths.py
   :linenos:
   :emphasize-lines: 10

We see here a pattern which is common with |testix| - specifying an
entire scenario of what should happen, then making it happen by calling
the code under test.

Here's another version of the same test

.. literalinclude:: other_tests/more_advanced/1/test_forward_lengths_2.py
   :linenos:

You should use the style that makes the test most readable to you.

For later reference, here's the code that passes this test:

.. literalinclude:: other_tests/more_advanced/1/forwarder.py

Exactness
---------

What happens if we now change the code above to read

.. literalinclude:: other_tests/more_advanced/2/forwarder.py
   :linenos:
   :emphasize-lines: 6

That is, we decided we want to close the outgoing socket for some reason.

.. code:: console

   $ python -m pytest -v docs/tutorial/other_tests/more_advanced/2/test_forward_lengths.py

    ...


        def _fail_py_test( exceptionFactory, message ):
    >       return pytest.fail( message )
    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: incoming_socket.recv(4096)
    E        actual  : outgoing_socket.close()
    E       === OFFENDING LINE ===
    E        write_to.close() (/home/yoav/work/testix/docs/tutorial/other_tests/more_advanced/2/forwarder.py:6)
    E       === FURTHER EXPECTATIONS (showing at most 10 out of 3) ===
    E        outgoing_socket.send(b'10 ')
    E        incoming_socket.recv(4096)
    E        outgoing_socket.send(b'14 ')
    E       === END ===


As you can see, the test fails, and the new ``.close()`` is now, in |testix| jargon, the "offending line".

This is because |testix| expectations are asserted in an *exact* manner - we define
*exactly* what we want, *no more - no less*.

This makes |testix| very conducive to Test Driven Development - if you change the code before changing the test - it will probably result in failures.
When approaching adding new features - start with defining a test for them.

We'll discuss exactness some more next.
