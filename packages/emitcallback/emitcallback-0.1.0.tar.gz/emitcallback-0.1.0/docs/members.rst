
Members Reference
=================

.. automodule:: emitcallback

.. hint::
	All classes supports being copied with Python's :py:mod:`copy` module.

.. warning::
	Connections with async callables or usage with threads aren't fully supported, and their usage
	hasn't been tested at all.

Other useful pages in this documentation:
- :doc:`glossary`
- :doc:`examples`

______

.. currentmodule:: emitcallback

.. autoclass:: Single
.. autoclass:: Signal
.. autoclass:: Queue

Constants
*********

.. autodata:: SINGLE_NO_WEAK
.. autodata:: SINGLE_ONE_SHOT

.. autodata:: SIGNAL_NO_WEAK
.. autodata:: SIGNAL_ONE_SHOT
.. autodata:: SIGNAL_MULTI_CONNECT
.. autodata:: SIGNAL_INTERRUPT_EXCEPTION

Exceptions
**********

.. autoexception:: AlreadyConnectedException
