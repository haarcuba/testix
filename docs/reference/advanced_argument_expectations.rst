.. include:: ../colors.rst
.. include:: ../common.rst

Advanced Argument Expectations
==============================

Most of our examples of working with ``Scenario`` expectations
are of *exact* matches, e.g.

.. code:: python

    s.classroom.set('A', index=9, name='Alpha')

Means we expect the ``.set()`` method to be called on the fake object ``Fake('classroom')`` with these *exact* arguments: a positional argument with the value ``'A'``, and two keyword arguments ``index=9, name='Alpha'``.

In most cases this is exactly what we want. However, sometimes we want something else. Let's see what |testix| supports.

Ignoring A Specific Argument
----------------------------

Sometimes we don't care about the value of a specific argument. For example,
we might want to verify that our code calls ``time.sleep()`` but we don't
want to test for a specific number of seconds.

Here's how to do this in |testix|:

.. code:: python

    with Scenario() as s:
        s.time.sleep(IgnoreArgument())
        # must call time.sleep() with one argument, but any value for this argument will be OK

You can also use this in a kwarg expectation

.. code:: python

    with Scenario() as s:
        s.greeter.greet('hello!', person=IgnoreArgument())
        # must use 'hello!', but any value for person will be OK

Ignoring All Call Details
-------------------------

What if we want to make sure a method is called, but we don't care about the arguments at all?
This is what ``IgnoreCallDetails()`` is for, e.g. this test expects the ``.connect()`` method to be called on the fake object ``Fake('database')`` three times, but specifies that it doesn't care about the exact arguments:

.. literalinclude:: argument_expectations/test_ignore_details.py
   :linenos:
   :emphasize-lines: 7-9


Here is an example of code that passes this test

.. literalinclude:: argument_expectations/server.py
   :linenos:

As you can see, the ``.connect()`` method is called three times, but with different arguments each time, and this satisfies the ``IgnoreCallDetails()`` expectation.

Testing for Object Identity
---------------------------

Sometimes we want to ensure a method is called with a specific object. We are not satisfied with it being 
called with an *equal* object, we want the *same actual object*. That is, we are interested in testing ``actual is expected`` and not ``actual == expected``.

We can do this with ``ArgumentIs``. Here is an example:


.. literalinclude:: argument_expectations/test_object_identity.py
   :linenos:
   :emphasize-lines: 9,17

We list here two tests, both demand that the object passed to ``mylist.append()`` will be the actual object ``joe`` created at the start of the test. The test ``test_this_will_fail()`` is made to fail on purpose by using the wrong method on the tested object, this is the code that passed (and fails) these tests:


.. literalinclude:: argument_expectations/classroom.py
   :linenos:
   :emphasize-lines: 5,6

If we didn't use ``ArgumentIs`` and just used


.. code:: python

        s.mylist.append(joe)

The ``test_this_will_fail()`` test would have passed, because ``joe`` is equal to the object passed to ``.append()`` as defined by the ``__eq__`` method. With ``ArgumentIs``, however, you will get something like this failure message:

.. code:: console

    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E        expected: mylist.append(|IS <classroom.Person object at 0x7f5162c2c5e0>|)
    E        actual  : mylist.append(<classroom.Person object at 0x7f5162c2c250>)


Capturing Arguments
-------------------

Sometimes we don't want to *demand* anything about a method's arguments, but we do want to *capture* them.
This is useful for when we want to simulate the triggering of an internal callback. 

For example, suppose we have a class which implements some logic when the process ends via an `atexit <https://docs.python.org/3/library/atexit.html>_` handler. 
Testing this might seem hard, since we don't want to actually make the process (which is running our test) exit.

Here's how to do it using |testix|'s ``SaveArgument`` feature.


.. literalinclude:: argument_expectations/test_atexit_handler.py
   :linenos:
   :emphasize-lines: 11,15-16,18

We use ``saveargument.SaveArgument()`` to capture the argument passed to ``atexit.register()``, and name this captured argument ``the_handler``.

We later retrieve the captured callback via the ``saveargument.saved()`` dictionary. 

This enables us to trigger the callback ourselves by calling ``handler()`` - which satisfies our demand ``s.cleanup_logic(1, 2, 3)``.

**NOTE** a simpler way might have been to make the ``_cleanup()`` function public, and then we could just call it: ``tested.cleanup()``. However, if this is not called in our code, we should not make it public, and since we are forbidden by good ethics from accessing a private function from outside the class, we need to capture it.

Implementing Arbitrary Argument Matching
----------------------------------------

Sometimes you need some complicated logic that |testix| doesn't support 
out of the box.

You can define your own argument expectation classes with some arbitrary logic, and use them in your tests, by implementing classes derived from the ``ArgumentExpectation`` base class, which is essentially an interface:


.. code:: python

    class ArgumentExpectation:
        def __init__(self, value):
            self.expectedValue = value

        def ok(self, value):
            # returns true if value meets the expectation, false otherwise
            raise Exception("must override this")

The following tests implements a new ``StartsWith`` expectation, which expects a string that starts with a given prefix.

.. literalinclude:: argument_expectations/test_arbitrary_argument_expectation.py
   :linenos:
   :emphasize-lines: 10-12,16

We demand that ``open()`` be called with a filename that starts with ``/tmp/``, and with *exactly* ``'w'`` as the second argument.

This code passes this test:

.. literalinclude:: argument_expectations/temporary_storage.py
   :linenos:
   :emphasize-lines: 3


The ``ArgumentExpectation`` base class implements a default ``__repr__`` function, but you can implement one yourself e.g.


.. code:: python

    class StartsWith(ArgumentExpectation):
        def ok(self, value):
            return value.startswith(self.expectedValue)

        def __repr__(self):
            return 'StartsWith({})'.format(repr(self.expectedValue))

Using this ``ArgumentExpectation`` interface, you can make |testix| support any arbitrary and complicated argument verification you need.
