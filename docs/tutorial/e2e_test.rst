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


Something like this. Let's write a test which uses two such clients, one for Alice and one for Bob

.. literalinclude:: ../chatapp/tests/e2e/pseudo/test_send_and_receive_messages.py
