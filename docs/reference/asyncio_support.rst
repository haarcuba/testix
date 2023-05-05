.. include:: ../colors.rst
.. include:: ../common.rst

AsyncIO Support
===============

|testix| offers support for testing asynchronous code, that is code which takes
advantage of Python's `async` and `await` keywords.

|testix|'s `async` support has been tested to work with `pytest-asyncio <https://github.com/pytest-dev/pytest-asyncio>`_.

AsyncIO Expectations
--------------------

You can specify that a method call should be awaited using the ``__await_on__`` modifer of the ``Scenario``,
as in the example below. As you can see, you may also mix and match sync and async expectations.

.. literalinclude:: async_tests/test_1.py
   :linenos:
   :emphasize-lines: 4,5,7-9

Note that the test function itself is `async` and that you have to use the
``pytest.mark.asyncio`` decorator on the test - this decorator makes
sure the test runs inside an ``asyncio`` event loop.

AsyncIO Context Managers
------------------------


