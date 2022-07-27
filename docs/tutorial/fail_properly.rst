Failing Properly
================

If we run our `E2E Test <e2e_test>`_ it will of course not work,
because none of the code for `chatapp` exits yet. This is a sort of failure, but it's not very interesing. 

What we want is for the test to fail *properly* - we want it to fail because our system isn't implemented yet - we want it to fail because messages are seemingly sent, but they don't arrive at their destination. In short, we want it to fail on our ``assert`` statements, not due to some technicalities

TBD
