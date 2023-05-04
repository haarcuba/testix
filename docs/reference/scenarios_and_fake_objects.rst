.. include:: ../colors.rst
.. include:: ../common.rst

Basic Usage: Scenarios and Fake Objects
=======================================

Scenarios and Fake Objects
--------------------------

|testix| is a mocking framework designed to support the TDD style of programming. When writing a test with |testix|, we use a `Scenario()` object to specify *what should happen* or what we *expect* should happen when the tested code is run. We can refer to these as *demands* or *expectations*.

Here's a test that expects the tested code to repeatedly call ``.recv(4096)`` on a socket, until an empty sequence is returned, and then call ``.close()`` on the socket. Furthermore, ``tested.read()`` should return the accumulated data.

.. literalinclude:: 1/test_reader.py
   :linenos:

Scenarios track fake objects - instances of ``Fake``. Fake objects have a name, e.g. ``Fake('sock')`` - and you can demand various method calls on a fake object, e.g.

    
.. code:: python

    s.sock.recv(4096) >> b'data1'

Means "we require that the ``.recv()`` method be called on the fake object named ``'sock'`` with exactly one argument: the number 4096. When this happens, this function call will return ``b'data1'`` to the caller".

Note this last part - when we define an *expectation*, we may also define the return value returned should the expectation come true.

The code which passes this test is

.. literalinclude:: 1/reader.py
   :linenos:


The ``Scenario()`` object helps us define our expectations from our code, and also *enforces* these expectations when used, as above, in a ``with Scenario() as s`` statement. When the ``with`` ends, the ``Scenario`` object will make sure that *all expectations have been exactly met*.

Try to comment out some lines in the ``Reader`` class, and you will see that the test no longer passes. E.g. if you comment out the ``.close()`` call you will get


.. code:: console

    >       return pytest.fail( message )
    ...
    E       Scenario ended, but not all expectations were met. Pending expectations (ordered): [sock.close()]

|testix| tells you that not all expectations were met, like it should.

More Complex Expectations
-------------------------

You can specify any number of arguments, and also keyword arguments, e.g.


.. code:: python

    s.alpha.func1(1, 2, a=1, b='hi there')

This will ensure that the ``.func1()`` method is called on the ``Fake("alpha")`` object *exactly* like this:

.. code:: python

    def my_code(a):
        a.func1(1, 2, a=1, b='hi there')

With this definition, ``my_code(Fake("alpha"))`` will pass the test. The value returned from ``.func1()`` in this case will be ``None``. If you want to specify a return value, use ``>>`` as before
    
.. code:: python

    s.alpha.func1(1, 2, a=1, b='hi there')

Overriding Imported Modules With Fake Objects
---------------------------------------------

Since ``Scenario`` can only track ``Fake`` objects, the tested code must have access to them. We already saw one way this can happen, when we pass in a fake, e.g.

.. code:: python

        tested = reader.Reader(Fake('sock'))

Another common pattern with |testix| is to override some global names inside the tested module - this essentially overrides ``import`` statements.

Here is an example of overriding the ``socket`` import using |testix|'s ``patch_module`` pytest `fixture <https://docs.pytest.org/en/7.1.x/explanation/fixtures.html#about-fixtures>_`. This test demands that the ``MyServer()`` object create a socket, listen on it, accept a connection, send ``b'hi'`` over this connection, then close it.

.. literalinclude:: override_import/test_override_socket.py
   :linenos:
   :emphasize-lines: 5-7

**NOTE**: The ``patch_module`` helper will, when the test is over, return the original object to its place. It's important to use ``patch_module`` and not do it yourself.

Another important point is that ``patch_module`` overrides global names, go, e.g. if we use ``patch_module`` like this

.. code:: python

    patch_module(my_module, 'xxx')

And ``my_module`` has this code

.. code:: python

   xxx = 300

   def get_xxx():
       return xxx

Then ``xxx`` will not be 300 for the duration of the test, but instead have a fake object by the same name ``Fake("xxx")``.

This will also be the case if ``my_module`` had

.. code:: python

   from important_constants import xxx

   def get_xxx():
       return xxx


Using ``patch_module`` With Arbitrary Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usually we use ``patch_module`` to override module-level names with Fake objects, but you can specify any object as the override

.. code:: python

    patch_module(my_module, 'xxx', 500) # override xxx value with 500

The Most Common Ways To Create Fake Objects
-------------------------------------------

So, Fake objects can be created and passed in directly, they can be used to mock imported modules using ``patch_module``, and they can be returned as the result of another Fake object call, e.g. the line

.. code:: python

        s.socket.socket() >> Fake('server_sock')

In fact, in this line as well as in the one that follows:

.. code:: python

        s.server_sock.accept() >> (Fake('connection'), 'some address info')

There is, in fact, another method that creates Fake objects. The preceding line specifies that ``server_sock.accept`` is called - which, under the hood, implies the creation of a ``Fake("server_sock.accept")`` fake object.

To summarize, the main modes where fakes are created are:

#. Created and passed in directly
#. Created and returned as the return value of an expectation
#. Replacing a global name (usually an imported module) using ``patch_module``
#. Implicitly created when addressing a method of a fake object, e.g. ``server_sock.accept`` above.






Less Strict Expectations
========================

Less Specific Arguments
-----------------------

Sometimes you want to specify an expectation, but with less strict demands.

Continuing with the previous example, maybe we don't care that much that ``4096`` be used when calling ``.recv()``

This can be accomplished using ``IgnoreArgument()``, e.g.

.. literalinclude:: 2/test_reader.py
   :linenos:

You can also use ``IgnoreArgument()`` to specify that you demand some kwarg be used, but you don't care about it's value

.. code:: python

    s.alpha.func1(1, 2, a=IgnoreArgument(), b='hi there')

    # must use (1, 2, a=<any object here>, b='hi there')


Unordered Expectations
----------------------

Most of the time, in my experience, it's a good idea that expectations
are met in the exact order that they were specified. 

.. code:: python

    s.alpha.func1(1, 2)
    s.alpha.func2('this must come after func1')

These expectations will only be met if ``.func2()`` is called after ``.func1()`` was called.


However, sometimes we want to relax this a little, and demand that some function is called, but you don't care if it's before or after some other function. You can do this by using the ``.unordered()`` modifier:

.. literalinclude:: 3/test_unordered.py
   :linenos:
   :emphasize-lines: 7

This demands that the fake is called with ``'b'`` only *after* it was called with ``'a'`` - but it forgives the call with ``'c'`` - you can call the fake with ``'c'`` before, after on in between the ``'a'`` and ``'b'`` calls.

The code in ``my_code()`` passes this test.



Context Manager Expectations
----------------------------

Sometimes we want to demand that an object is used as a context manager in a ``with`` statement.

Here's an example of how to demand this on a fake object named ``'locker'``, using ``Scenarios`` special ``__with__`` modifier, along with the code that passes the test.

.. literalinclude:: 4/test_locker_context_manager.py
   :linenos:
   :emphasize-lines: 6
