.. include:: colors.rst
.. include:: common.rst

|testix|
========
The Test-First Mocking Framework
--------------------------------

|testix_bold| is the Test-First (TDD) Friendly Mocking framework for Python, meant to be used with pytest_

.. _pytest: https://docs.pytest.org/en/latest/



|testix| is special because it allows you to specify what your mock objects do,
and it then enforces your specifications automatically. It also reduces (albeit
not entirely) mock setup.

Other frameworks usually have a flow like this:

#. setup mock
#. let code do something with mock
#. assert mock used in correct way

|testix| flow is a bit different

#. setup mock objects
#. specify *exactly* what should happen to them using a Scenario context


Quick Example
-------------

Here is a quick example of how |testix| works.

.. code:: python

    # to test the Chatbot class, we pass it a mock socket called "sock"
    tested = chatbot.Chatbot(Fake('sock'))

    # create a Scenario context
    # inside, you specify exactly what the unit should do with the objects its handed
    with Scenario() as s:

        s.sock.recv(4096) >> 'request text'  # unit must call sock.recv(4096).
                                             # this call will return 'request text'
        s.sock.send('response text')

        # call your unit's code
        tested.go()


    # Scenario context ends, and verifies everything happened exactly as specified
    # No more, no less

Note that you do not have to setup ``sock.recv`` or ``sock.send`` - once ``sock`` is
set up, it will generate other mock objects automatically as you go along with
it. Only "top level" mock objects need to be setup explicitly.

The ``Scenario`` object does essentially two things:

#. setup our expectations (these are the ``s.sock.*`` lines)
#. enforce our expectations (this is done by the ``with`` statement)

Want to know more? Read the :doc:tutorial.

Some Advanced Features
----------------------

|testix| natively and elegantly supports testing for

#. Context managers (``with`` statement constructs)
#. ``async`` code
#. ``async`` context managers (``async with`` statement constructs)
#. Hooks - allowing you to simulate asynchronous events that happen between two lines of your code


Advantages
----------

|testix| has been written to promote the following

#. Readability - the expectations are very similar to the actual code that they
   test (compare ``s.sock.recv(4096)`` with the standard ``sock.recv.assert_called_once_with(4096)``
#. Test Driven Development friendliness: if you use ``sock.recv.assert_called_once_with(4096)``, you must
   use it after the code has run. With |testix|, you specify what you *expect*, and the asserting
   is done for you by magic.

What are you waiting for?


Go to the :doc:`reference<reference/index>` or read the :doc:`Tutorial<tutorial/index>`

Read More
---------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference/index
   tutorial/index
