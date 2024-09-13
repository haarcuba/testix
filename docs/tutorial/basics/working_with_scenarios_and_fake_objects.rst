.. include:: ../../colors.rst
.. include:: ../../common.rst

Working With Scenarios and Fake Objects
=======================================

In this part we introduce the basic building blocks of writing a unit test with
|testix|.  As mentioned in :ref:`unit_tests`, this is where we test our business logic: the required behaviour and edge cases. To control carefully how our code interacts with the outside world, we use so called Mock objects or as they are sometimes called Fake objects.

Before seeing how |testix| does it, let's review the concept of Mock objects.

Mock Objects
------------

Mock Objects are objects that simulate some object that our code needs
to interact with, that we want to test carefully. As an example - suppose our code needs to send data over a socket, which it receives as a parameter called ``sock``


.. code:: python

    send_some_data(sock, b'the data')

When testing we

#. don't *really* want to send data over a *real* socket
#. do want to verify that the ``send_some_data`` function called ``sock.send(b'the data')``.

The solution is to pass ``send_some_data`` an object that implements a ``.send`` method, but which is not an actual socket. Instead this object will just record that ``.send`` was called, and we'll be able to query it to see that it was called with ``b'the data'``. The idea here is that there's no point testing sockets - we know that those work. The point here is to test that *our code does the right thing with the socket*.

The Standard Library Way - `unittest.mock`
------------------------------------------

The approach taken by the standard `unittest.mock <https://docs.python.org/3/library/unittest.mock.html>`_ module from the Python standard library,
is to provide us with a generic ``Mock`` class which records every call that is made to it, and has some helper functions
to help as `assret` that some things happened.


.. code:: python

    import unittest.mock

    def test_sending_data():
        sock = unittest.mock.Mock()
        send_some_data(sock, b'the data')
        sock.send.assert_called_with(b'the data') # this verifies that `send_some_data` did the right thing

Let's see how |testix| approaches the same idea. We will discuss the advantages of the |testix| way later on.

Testix Fake Objects and Scenarios
---------------------------------

Setting the Expectations
************************

We'll start by introducing a test for ``send_some_data`` and then explaining it.

Note that first we need to fail the test - so ``send_some_data`` here is only a skeleton implementation that really does nothing.

.. literalinclude:: other_tests/data_sender_example/1/test_sending_data.py
   :linenos:
   :caption: test_sending_data.py
   :emphasize-lines: 7,8,10

.. literalinclude:: other_tests/data_sender_example/1/data_sender.py
   :caption: data_sender.py skeleton implementation


What's going on here? First, we create a `Fake` object ``sock`` - this is |testix| generic mock object - note that we
define a name for it explicitly - ``'sock'``. We then start a ``Scenario()`` context manager in the ``with Scenario() as s`` statement.

A Scenario is a way to specify the required behaviour - what do we demand happen to our fake objects? In this case,
we specify one demand:

.. code:: python

   s.sock.send(b'the data')

This means - we expect that the Fake object method ``sock.send`` be called with ``b'the data'`` as the argument. When the ``Scenario``
context ends - the ``Scenario`` object will automatically enforce these expectations, as we'll see shortly.

Finally - we cannot hope to meet the demands of the test without actually calling the code:



.. code:: python

   send_some_data(fake_socket, b'the data')

Let's try to run this test. Of course we expect failure - the ``send_some_data`` function does not, after all, send the data.


.. code-block:: console

    $ python -m pytest -v docs/tutorial/other_tests/data_sender_example/1


    ....... OUTPUT SKIPPED FOR BREVITY .......
    E       Failed:
    E       testix: ScenarioException
    E       testix details:
    E       Scenario ended, but not all expectations were met. Pending expectations (ordered): [sock.send(b'the data')]




As you can see, |testix| tells us that "not all expectations were met", and details the missing expectation in a list: ``sock.send(b'the data')``.

We have a **properly failing test**, yay!


Meeting the Expectations
************************

Now that we know that the test's expecations aren't being met - let's change the code to meet them:


.. literalinclude:: other_tests/data_sender_example/2/data_sender.py
   :caption: meet the demand for sending data
   :emphasize-lines: 2

Now our tests pass


.. code-block:: console

    python -m pytest -v docs/tutorial/other_tests/data_sender_example/2

    docs/tutorial/other_tests/data_sender_example/2/test_sending_data.py::test_sending_data PASSED


Yay :)

Let's say that now we want our sending function to send a specific header before the data which specifies the data's length.
Since we're doing TDD here, we first set our expectations in the test

.. literalinclude:: other_tests/data_sender_example/prefix_0/test_sending_data.py
   :linenos:
   :caption: testing for a header
   :emphasize-lines: 8

Now our scenario demands that `send()` be called twice - once with the header, and then with the data.

Next move - let's see that our test fails properly. When we run it we get

.. code-block:: console

    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: sock.send(b'SIZE:8 ')
    E        actual  : sock.send(b'the data')
    E       === OFFENDING LINE ===
    E        socket.send(data) (/home/yoav/work/testix/docs/tutorial/tests/data_sender.py:2)
    E       === FURTHER EXPECTATIONS (showing at most 10 out of 1) ===
    E        sock.send(b'the data')
    E       === END ===


What happened here? Well, the scenario wants to see ``sock.send(b'SIZE:8 ')`` - however, since
we have not changed our code yet, the actual call is the good old ``sock.send(b'the data')``, therefore
the *expected* call is different from the *actual* call, and |testix| fails the test for us. It also
specifies the particuar line that got us in trouble, and gives us a peek into the next expecations in the scenario.

Good news, we have a properly failing test. Now, let's meet the demands:

.. literalinclude:: other_tests/data_sender_example/prefix_1/data_sender.py
   :linenos:
   :caption: sending a header 1
   :emphasize-lines: 3,4


OK let's go:

.. code-block:: console

    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: sock.send(b'SIZE:8 ')
    E        actual  : sock.send(b'SIZE:8')
    E       === OFFENDING LINE ===
    E        socket.send(header) (/home/yoav/work/testix/docs/tutorial/tests/data_sender_prefix.py:5)
    E       === FURTHER EXPECTATIONS (showing at most 10 out of 1) ===
    E        sock.send(b'the data')


Oops! Seems like we forgot a ``b' '``, let's correct our code:

.. literalinclude:: other_tests/data_sender_example/prefix_2/data_sender.py
   :linenos:
   :caption: sending a header 2
   :emphasize-lines: 5

Now the test passes.

.. code-block:: console

    $ python -m pytest -v docs/tutorial/other_tests/data_sender_example/prefix_2

    docs/tutorial/other_tests/data_sender_example/prefix_2/test_sending_data.py::test_sending_data PASSED
