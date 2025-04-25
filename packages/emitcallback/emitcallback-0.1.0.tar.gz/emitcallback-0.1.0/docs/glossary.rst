
Glossary
========

Common terms and principles used by implementations in this library.

Connection & Disconnection
	When a callable object is being set, added or removed as a target for an emittion.

	The connection is created and stored inside the object, it's a direct reference to the callable target and optionally the flags being used.

	Disconnection will happen automatically when the oneshot tag is enabled or a connection's weakreference dies.

Weak reference to a callable
	Reffering to Python's weak reference and weakref module.

	Class instance methods are used exclusively with weak references so when an instance is no longer being used in the code his method(s) are automatically removed from any connection.

	This allows the garbage collection to properly remove those objects, a whole reference can still be used when the no weak reference tag is active.

Emittion
	Is the process of calling the connected callables and is made of these steps.

	1. Disconnect if the oneshot tag is enabled.
	2. Calls each connected callable passing the emittion argouments.
	3. Raise all connected exceptions from the callables.

Emittion exception
	Always done with Python's ExceptionGroup on sequences, otherwhise it may use the callable's raised exception.

Flags
	Options applied to a connection, here shortly described:

	* oneshot
		Disconnect the callable before being called, prevents any next emittion to call that connection again.
	* interrupt on exception
		Will interrupt a sequence of calls from an emittion if the callable raises any exception.
	* no weak
		Always uses a whole reference to a callable, related for weak methods on classes.
	* multi connect
		Allows connecting multiple times the same unique callable.
