Failing Properly
================

If we run our `E2E Test <e2e_test>`_ it will of course not work:

.. code-block:: console

   $ python -m pytest docs/chatapp/tests/e2e/test_send_and_receive_messages.py

Results ultimately in

.. code-block:: console

    E   ModuleNotFoundError: No module named 'chatapp'


That is because none of the code for `chatapp` exits yet. This is a sort of failure, but it's not very interesting. 

What we want is for the test to fail *properly* - we want it to fail *not* because our system doesn't exist - we want it to fail because our system does not implement the correct behaviour yet. 

In concrete terms, we want it to fail because messages are seemingly sent, but they don't arrive at their destination. In short, we want it to fail on our ``assert`` statements, not due to some technicalities

So, let's write some basic code that achieves just that. We create the following directory tree:

.. code-block:: console

    chatapp
    ├── __init__.py
    ├── client.py
    └── server.py

With skeleton code:

.. literalinclude:: ../chatapp/source/chatapp/client.py
   :linenos:
   :caption: client.py

.. literalinclude:: ../chatapp/source/chatapp/server.py
   :linenos:
   :caption: server.py

Now if we run the test:


.. code-block:: console

    $ python -m pytest docs/chatapp/tests/e2e/test_send_and_receive_messages.py


We get a proper failure

.. code-block:: console

    ....... OUTPUT SKIPPED FOR BREVITY .......

    >       assert alice_callback.messages == [{'message': 'hi Alice', 'peer': 'Bob'}]
    E       AssertionError: assert [] == [{'message': ...peer': 'Bob'}]
    E         Right contains one more item: {'message': 'hi Alice', 'peer': 'Bob'}
    E         Use -v to get the full diff

    docs/chatapp/tests/e2e/test_send_and_receive_messages.py:32: AssertionError


This is a **proper failure**, messages were sent, but none arrived.


The Importance of Proper Failure
--------------------------------

Congratulations, we have a **failing test**! This is the first milestone when developing a feature in Test Driven Development. Let's briefly explain whey this is so important, and why this is superior to writing tests for previously written, already working code.

Essentially, imagine we wrote a test, wrote some skeleton code, ran the test - and it *didn't fail*. Well, that would obviously mean that our test was bad. This is admittedly rare, but I've seen it happen.

The more common scenario however is that we wrote the test, wrote the skeleton code, ran the test - and it failed, but *not in the way we planned*. This means that the test does not, in fact, test what we want. 

If we write our test *after* we've developed our code, how will we ever know that the test actually tests what we think it is testing? You'd be amazed at the number of tests which exist out there and in fact, do not test what they are supposed to.
I have seen with my own eyes, more than once, tests that do not test *anything at all*.

But if we write our tests first, and **fail them properly**,

* we make sure they actually test what they are supposed to
* we let the test drive the design of the application
* we take pains to actually think about how the code will be used

So, it is essential before developing some behaviour, that our tests fail properly.

Now, let's get on with implementing the application. 
We'll start with the server.
