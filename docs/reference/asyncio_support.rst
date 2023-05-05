.. include:: ../colors.rst
.. include:: ../common.rst

AsyncIO Support
===============

|testix| offers support for testing asynchronous code, that is code which takes
advantage of Python's `async` and `await` keywords.

|testix|'s `async` support has been tested to work with `pytest-asyncio <https://github.com/pytest-dev/pytest-asyncio>`_.

AsyncIO Expectations
--------------------

You can specify that a method call should be awaited using the ``__await_on__`` modifier of the ``Scenario``,
as in the example below. As you can see, you may also mix and match sync and async expectations.

.. literalinclude:: async_tests/test_1.py
   :linenos:
   :emphasize-lines: 4,5,7-9

Note that the test function itself is `async` and that you have to use the
``pytest.mark.asyncio`` decorator on the test - this decorator makes
sure the test runs inside an ``asyncio`` event loop.

Note that the ``__await_on__`` changes the expectation ``.my_fake('some data')`` into *two* expectations - the function call, and the use of ``await``-ing. You can see this, if, e.g., you cut ``my_code(thing)`` short by replacing its first line with ``return 'sync value'``. This is the correct value, so the ``assert`` statement passes, however the ``Scenario`` context will inform you that 

.. code:: console

    E       Scenario ended, but not all expectations were met. Pending expectations (ordered):
    [my_fake('some data'), await on my_fake('some data')@cb28287a42fc(),
    another_fake(), await on another_fake()@94bb8afd7e45(),
    yet_another(), await on yet_another()@b09a73bf3ee0(),
    last_one.sync_func(1, 2, 3)]


You can see that every ``__await_on__`` results in a special expectation representing it.

AsyncIO Context Managers
------------------------

You can specify your expectation for an object to be used
as an `async` context manager (i.e. in an `async with` statement) by using the ``__async_with__`` modifier. Here's an example testing a module called ``async_read`` which has an async function ``go()`` which reads the contents of a file asynchronously.

.. literalinclude:: async_tests/test_async_context_manager.py
   :linenos:
   :emphasize-lines: 13

Note our use of ``patch_module`` to mock the `aiofiles <https://pypi.org/project/aiofiles/>`_ library, which we assume is imported and used by our ``async_read`` module.

The code which passes this test is

.. literalinclude:: async_tests/async_read.py
   :linenos:

**Note** you do not have to specify a return value with ``>>`` for the
``__async_with__`` expectation if you want to use the "anonymous" form of the
``async with`` statement:

.. code:: python

    async with lock(): # no "as" part
        await handle_critical_data()
