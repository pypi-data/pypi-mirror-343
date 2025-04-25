
Examples
========

Here a few examples to use this library functionality and type hints.

.. literalinclude:: examples/1_overview.py
  :language: py
  :caption: Simple overview to instance the connectable objects and connect them a function.
  :linenos:

.. literalinclude:: examples/2_connect_flags.py
  :language: py
  :caption: Connects twince the function using mutiple flags at once.
  :linenos:

.. code::

	# This on the first emittion.
	> "Hello World"
	> "Hello World"

	# This on the second emittiong, the first connection has been removed by oneshot.
	> "Hello World"

.. literalinclude:: examples/3_connectables.py
  :language: py
  :caption: Shows how each kind of callables can be connected.
  :linenos:

.. literalinclude:: examples/4_weak_connection.py
  :language: py
  :caption: Shows how a method weak connection works when the garbage collector destroy the object.
  :linenos:

.. literalinclude:: examples/5_strong_connection.py
  :language: py
  :caption: Shows how a method strong connection can be created.
  :linenos:

.. note::
	Functions and lambdas always use a strong connection, weak connections are only for methods.

.. literalinclude:: examples/20_type_hints.py
  :language: py
  :caption: Shows how to create a signal and function with type hints.
  :linenos:

.. code::

	> "Value is 10!"

.. literalinclude:: examples/21_type_hints_2.py
  :language: py
  :caption: More showcase of type hints.
  :linenos:
