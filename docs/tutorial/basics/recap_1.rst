.. include:: ../../colors.rst
.. include:: ../../common.rst

Recap
=====

We can now summarize the essentials of the |testix| approach:

#. use ``Fake`` objects to simulate various entities
#. use a ``Scenario`` object to define an exact set of demands or *expectations*
#. the ``Scenario`` object not only defines our expectations, it is also used in a ``with`` statement to *enforce* them.
#. return values from ``Fake`` objects may be specified using ``>>``.

By requiring the developer to define his or her demands using a the Scenario concept, |testix| lends itself in particular to Test Driven Development - think about testing first, write the code only after you have exactly defined what you want it to do.

We can also now recognize some major advantages over the mock objects from the Python Standard Library.

#. |testix| lends itself naturally to the Test Driven approach to development (TDD) through its ``Scenario`` concept and the "no less - no more" approach that makes it harder to change the functionality of code without changing the test first.
#. test syntax is more visually similar to the code under test, e.g. the ``s.sock.send(b'the data')`` is visually similar to the same as the actual code ``socket.send(data)``. This makes tests more readable and easy to understand.
#. Whatever expectations you define for you mock objects - they will be 
   *exactly enforced* - defining expectations and enforcing them *is one and the same*.
