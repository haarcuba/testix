.. include:: ../common.rst

End-to-End Test
================

When we say "Test First" - this means that we go 
about thinking about our code by thinking about how to test
that it works.

When we say "Test Driven" - this means that we 
let our thinking about tests *define* how the code will work.

In this way, the tests *drive* our development.

So, how should we go about testing that everything works in our chat app?
obviously, we should start the server, and send and receive some messages.

Let's think first about our client library, we will want some |Client| class
which will...


* work in its own thread
* receives a callback which will be called when there is a message available
* allows us to send a message to a friend
* every client is identified by a string, which is its *name*


.. code:: python

   def my_callback(client, message, peer):
        print(f'yay {client.name()} got a message from {peer}: {message}')

   my_client = Client(name='Alice', on_message=my_callback)
   my_client.send('hi', to='my_bestie')


Something like this. Let's write a test which uses two such clients, one for Alice and one for Bob. The
code below is not the final test, and will not really work, but it's a sketch:

.. literalinclude:: ../chatapp/tests/e2e/pseudo/test_send_and_receive_messages_1.py
   :linenos:

What do we have here? The idea is that, e.g., the ``alice`` client sends a message to ``Bob``, 
the message is relayed by our app, and when the ``on_message`` callback is called, it actually appends
the message to ``bob_messages``. The ``assert`` messages make sure that everything works as expected.

However, we are missing some thigns here:

* The ``on_message`` interface we defined before takes more arguments than just the message
* The ``assert`` statements run immediately after we send the messages - they could fail because the chat app takes a little while
* Finally, if we want teh app to relay messages, we need the server, not just clients

First, let's fix the ``on_message`` thing:


.. literalinclude:: ../chatapp/tests/e2e/pseudo/test_send_and_receive_messages_2.py
   :linenos:
   :emphasize-lines: 3-8,11-12,19-20

Nice. 

Now let's sleep a little to allow messages some time to get to us.

.. literalinclude:: ../chatapp/tests/e2e/pseudo/test_send_and_receive_messages_3.py
   :linenos:
   :emphasize-lines: 2,20-21

Finally, we will need to launch the server, and, come to think about it,
the clients will need to get the server URL to connect to. Since launching the server
is part of the *preperation* for the test (we need to *prepare* a running server so that
we can start testing) - this is a good ocasion to use pytest's `fixtures feature <https://docs.pytest.org/en/7.1.x/explanation/fixtures.html#about-fixtures>`_.

.. literalinclude:: ../chatapp/tests/e2e/pseudo/test_send_and_receive_messages_4.py
   :linenos:
   :emphasize-lines: 13-18,20,23-24

Tests Driving our Code
----------------------

Note that in the process of developing the *test*, we realized we need to add the
*server_url* parameter to the Client class. This is what we mean when we say
that tests *drive* development.

This is more or less the final form of our test, however to 
truly work Test Driven - we need to make this test *fail properly*. 
