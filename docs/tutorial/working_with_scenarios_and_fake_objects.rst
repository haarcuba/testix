.. include:: ../common.rst

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

* don't *really* want to send data over a *real* socket
* do want to verify that the ``send_some_data`` function called ``sock.send(b'the data')``. 

The solution is to pass ``send_some_data`` an object that implements a ``.send`` method, but which is not an actual socket. Instead this object will just record that ``.send`` was called, and we'll be able to query it to see that it was called with ``b'the data'``.

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

We'll start by introducing a test for ``send_some_data`` and then explaining it.
For brevity, we put the test and the functions it is testing, ``send_some_data``, in the same file (when we
return to our ``line_monitor`` we'll do it more realistically).

Note that first we need to fail the test - so ``send_some_data`` here is only a skeleton implementation that really does nothing.

.. literalinclude:: tests/test_sending_data.py
   :linenos:
   :caption: test_sending_data.py
   :emphasize-lines: 7,8,9,11

What's going on here? First, we create a `Fake` object ``sock`` - this is |testix| generic mock object - note that we 
define a name for it explicitly - ``'sock'``. We then start a ``Scenario()`` context manager in the ``with Scenario() as s`` statement.

A Scenario is a way to specify the required behaviour - what do we demand happen to our fake objects? In this case,
we specify one demand:

.. code:: python

   s.sock.send(b'the data')

This means - we demand that the Fake object method ``sock.send`` be called with ``b'the data'`` as the argument. When the ``Scenario``
context ends - the ``Scenario`` object will automatically enforce these demands, as we'll see shortly.

Finally - we cannot hope to meet the demands of the test without actually calling the code:



.. code:: python

   send_some_data(fake_socket, b'the data')

Let's try to run this test. Of course we expect failure - the ``send_some_data`` function does not, after all, send the data.


.. code-block:: console

    $ python -m pytest docs/tutorial

    ....... OUTPUT SKIPPED FOR BREVITY .......
    E       Failed:
    E       testix: ScenarioException
    E       testix details:
    E       Scenario ended, but not all expectations were met. Pending expectations (ordered): [sock.send(b'the data')]


 As you can see, |testix| tells us that "not all expectations were met", and details the missing expectation in a list: ``sock.send(b'the data')``.

 We have a **properly failing test**, yay!
