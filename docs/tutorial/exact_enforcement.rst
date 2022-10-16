.. include:: ../common.rst

Exact Enforcement
=================

|testix| enforces function calls which are specified in a Scenario.
It enforces

* the order in which calls are made
* the exact arguments, positional and keyword, which are used
* unexpected calls are considered a failure

Wrong Arguments
---------------

So, e.g. if we have a test like this:

   
.. literalinclude:: other_tests/more_advanced/3/test_exact_enforcement.py
   :linenos:

The code *must* be some variation of 


.. code:: python

        names = name_source.get_names('all', order='lexicographic', ascending=True)
        # and at some point later...
        name_destination.put_names(names)
        
any of these will cause a failure:

.. code:: python

        name_source.get_names('all', 'lexicographic', True)       # lexicographic should be a keyword argument
        name_source.get_names('all', True, order='lexicographic') # ascending should be a keyworkd argument
        name_source.get_names(spec='all', order='lexicographic', ascending=True) # spec is unexpected

Unexpected Calls
----------------

This code will also make the test fail:

.. code:: python

    def go(source, destination):
        names = source.get_names('all', order='lexicographic', ascending=True)
        destination.put_names(names)
        destination.something_else()

and |testix| will report

.. code-block:: console

    E       Failed:
    E       testix: ExpectationException
    E       testix details:
    E       === Scenario (no title) ===
    E       unexpected call: destination.something_else()
    E       Expected nothing

That is, the ``Scenario``'s various expectations were met, but then the code
"surprised" |testix| with another call on a ``Fake`` object.

As we said before, the right way to specify |testix| Scenarios as to 
specify what you want *exactly* - *no more, no less*.

Ways Around Exactness
---------------------

Sometimes, this exactness is too much - |testix| supports ways around this, but
most of the time, it is good to be exact. These features are
out of the scope of this tutorial, and are documented separately.
