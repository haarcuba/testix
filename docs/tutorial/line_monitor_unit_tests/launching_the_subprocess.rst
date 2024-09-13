.. include:: ../../colors.rst
.. include:: ../../common.rst

Launching the Subprocess
========================

High Level Design
-----------------

We will implement ``LineMonitor`` as follows:

#. a ``LineMonitor`` sill launch the subprocess using the `subprocess <https://docs.python.org/3/library/subprocess.html>`_ Python standard library.
#. It will attach a |pseudoterminal| to said subprocess (using `pty <https://docs.python.org/3/library/pty.html>`_). If you don't know too much about what a |pseudoterminal| is - don't worry about it, I don't either.

Essentially it's attaching the subprocess's input and output streams to the father process. Another way of doing this is using pipes, but there are some technical advantages to using a |pseudoterminal|.

#. it will monitor the terminal using ``poll()`` from the standard Python library's `select <https://docs.python.org/3/library/select.html>`_ module. This call allows to you check if the |pseudoterminal| has any data available to read (that is, check if the subprocess has written some output).
#. when data is available, we will read it line by line, and send it to the registered callbacks.


Let's start by working on the launching a subprocess with an attached |pseudoterminal|.

Implementation
--------------

First step is to launch the subprocess with an attached |pseudoterminal|. Let's write a test for that.
We want to enforce, using |testix|, that ``subprocess.Popen()`` is called with appropriate arguments.

If the following paragraph is confusing, don't worry - things will become clearer after you see it all working.

Since |testix|'s ``Scenario`` object only tracks |testix| `Fake` objects, we must somehow fool the ``LineMonitor`` to
use a ``Fake('subprocess')`` object instead of the actual ``subprocess`` module. We need to do the same for the ``pty`` module.


There's more than one way of doing this, but here we will use |testix|'s helper fixture, ``patch_module``.


.. literalinclude:: ../../line_monitor/tests/unit/1/test_line_monitor.py
   :linenos:
   :emphasize-lines: 7-9,14-15

What's going on here?

#. First, we use ``patch_module`` to mock imported modules ``subprocess`` and ``pty``, as described above. Note that our test function depends on ``override_imports`` to make everything work.
#. In our ``Scenario`` we demand two things:

    * That our code calls ``pty.openpty()`` to create a |pseudoterminal| and obtain its two file descriptors.
    * That our code then launch a subprocess and point its ``stdout`` to the write file-descriptor of the |pseudoterminal| (we also demand ``close_fds=True`` wince we want to fully specify our subprocess's inputs and outputs).

#. Finally, we call our ``.launch_subprocess()`` method to actually do the work -  we can't hope that our code meet our expectations if we never actually call it, right?

A few points on this:

#. See how we *first* write our expectations and only *then* call the code to deliver on these expectations. This is one way |testix| pushes you into a Test Driven mindset.
#. In real life, ``pty.openpty()`` returns two file descriptors - which are *integers*. In our test, we made this call return two *strings*.

  We could have, e.g. define two constants equal to some integers, e.g. ``WRITE_FD=20`` and ``READ_FD=30`` and used those - but it wouldn't really matter and would make the test more cluttered.
  Technically, what's important is that ``openpty()`` returns a tuple and we demand that the first item in this tuple is passed over to the right place in the call to ``Popen()``.
  Some people find fault with this style. Personally I think passing strings around (recall that in Python strings are immutable) where all you're testing is moving around objects - is a good way to make a readable test.

Failing the Test
~~~~~~~~~~~~~~~~

Remember, when practicing TDD you should always fail your tests first, and make
sure they :doc:`fail properly <../fail_properly>`.

So let's see some failures! Let's see some |RED|!

Running this test with the :ref:`skeleton implementation <skeleton_line_monitor>` we have for ``LineMonitor`` results in:

.. code-block:: console

    E       Failed:
    E       testix: ScenarioException
    E       testix details:
    E       Scenario ended, but not all expectations were met. Pending expectations (ordered): [pty.openpty(), subprocess.Popen(['my', 'command', 'line'], stdout = 'write_to_fd', close_fds = True)]

Very good, our tests fails as it should: the test expects, e.g. ``openpty()``
to be called, but our current implementation doesn't call anything - so the
test fails in disappointment.

Now that we have our |RED|, let's get to |GREEN|.

Passing the Test
~~~~~~~~~~~~~~~~

Let's write some code that makes the test pass:

.. literalinclude:: ../../line_monitor/source/2/line_monitor.py
   :linenos:
   :emphasize-lines: 9-12

Running our test with this code produces

.. code-block:: console

    test_line_monitor.py::test_lauch_subprocess_with_pseudoterminal PASSED

Finally, we see some |GREEN|!

Usually we will now take the time to |REFACTOR| our code, but we have
so little code at this time that we'll skip it for now.

OK, we have our basic subprocess with a |pseudoterminal| - now's
the time to test for and implement actually monitoring the output.
