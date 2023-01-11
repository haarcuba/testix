.. include:: ../../colors.rst
.. include:: ../../common.rst

Better Monitoring
=================

If you try working with our current ``LineMonitor`` implementation
you will find it has some disadvantages.

#. There is no way to stop monitoring.
#. In particular, if the underlying subprocess crashes, the monitor will just block for ever - it is blocked trying to ``.readline()`` - but the line will never come.

Furthermore, we originally wanted the ability to have more than one callback.

Let's improve our ``LineMonitor``, starting by handling the underlying subprocess a little more carefully.

TBD
