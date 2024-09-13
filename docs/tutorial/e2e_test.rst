.. include:: ../colors.rst
.. include:: ../common.rst

.. _e2etest:

End-to-End Test
================


When we say "Test First" - this means that we go
about thinking about our code by thinking about how to test
that it works.

When we say "Test Driven" - this means that we
let our thinking about tests *define* how the code will work.

In this way, the tests *drive* our development.

So, how should we go about testing that everything works in our ``LineMonitor`` library?
obviously, we should launch a subprocess which known output, and see that we can get all the lines emitted into a callback which we define.

So we want our users to do something like this

.. code:: python

   import line_monitor.monitor

   captured_lines = []

   monitor = line_monitor.LineMonitor(['ls', '-l'], on_output=captured_lines.append) # launch `ls -l` to list the files, lines get appended into our captured_lines list
   monitor.monitor() # monitor process until it ends
   for line in captured_lines:
        print(f'saw this: {line}')


Now that we have a rough idea, let's write a test which will make this precise. The code below is not the final test, and will not really work, but it's a sketch:

.. literalinclude:: ../line_monitor/tests/e2e/test_line_monitor.py
   :linenos:
   :caption: end-to-end (E2E) test
   :emphasize-lines: 5,6,9,11

What do we have here? We create the tested object, a ``LineMonitor`` object called ``tested``. We provide it a callback (which is just the ``.append`` method on the ``captured_lines`` list). We then tell it to launch the subprocess with similar arguments to ``subprocess.Popen`` - and we give it a specific subprocess which we know will print 10 lines of output. Finally, after the subprocess has ended we test that the captured output is what we expect it to be.

Tests Driving our Code
----------------------

Note that in the process of developing the *test*, we chose the names of various API calls, e.g. ``launch_subprocess`` (we could have launched the subprocess in the constructor like in the draft we wrote before, but it felt more natural to me to separate the creation of a ``LineMonitor`` object from actual launching of a subprocess).

This is what we mean when we say that tests *drive* development.

However, to truly work Test Driven - we need to make this test *fail properly*.
