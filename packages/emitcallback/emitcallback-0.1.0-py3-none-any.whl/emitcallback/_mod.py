from __future__ import annotations
from inspect import ismethod
from weakref import WeakMethod
from typing import Any, Callable

type CallbackType[**P, R] = Callable[P, R] | WeakMethod[Callable[P, R]]

def weakify[**P, R](
	callback: Callable[P, R],
	weakdead: Callable[[WeakMethod[Callable[P, R]]], None]
	) -> CallbackType[P, R]:

	return \
		WeakMethod(callback, weakdead) if ismethod(callback) \
		else callback

def unweak[**P, R](callback: CallbackType[P, R]) -> Callable[P, R]:

	return callback() if isinstance(callback, WeakMethod) else callback # type: ignore

class AlreadyConnectedException(Exception):
	""" exception raised when a callable object is already connected. """

	pass

SINGLE_NO_WEAK: int = 1
""" always use a reference to the callable object. """
SINGLE_ONE_SHOT: int = 2
""" disconnects the callable before being emitted. """

class Single[**P]:
	""" object that wraps only one callable or none. """

	def __init__(self, callback: Callable[P, Any] | None = None, flags: int = 0) -> None:

		self.__flags: int = flags
		self.__connection: CallbackType[P, Any] | None = None \
			if callback is None else \
				weakify(callback, self.__weakconnect_dead__) if (flags & SINGLE_NO_WEAK) == 0 \
				else callback

	def __weakconnect_dead__(self, ref: WeakMethod[Callable[P, Any]]) -> None:
		# internal method that erase a dead reference connection.

		if self.__connection == ref:
			self.__connection = None

	def connect(self, callback: Callable[P, Any], flags: int = 0) -> None:
		""" overrides the current connection with another callable and sets the connection tags.

		will always connect with a reference when :const:`SINGLE_NO_WEAK` is enabled.
		"""

		self.__flags = flags
		self.__connection = weakify(callback, self.__weakconnect_dead__) \
			if (flags & SINGLE_NO_WEAK) == 0 else callback

	def disconnect(self, callback: Callable[P, Any]) -> None:
		""" removes the current connection if the callable matches. """
		
		if not self.__connection is None and unweak(callback) == self.__connection:
			self.__connection = None

	def disconnect_any(self) -> None:
		""" removes any current connection. """
		
		self.__connection = None

	def is_connected(self, callback: Callable[P, Any]) -> bool:
		""" checks if the current connection matches the callable. """

		return unweak(callback) == callback

	def is_connected_any(self) -> bool:
		""" checks if there's is a connection with a callable. """

		return not self.__connection is None

	__contains__ = is_connected

	def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
		""" calls the current connection with the argouments.

		removes the connection first if :const:`SINGLE_ONE_SHOT` is enabled.

		will raise any exception thrown by the callable.
		
		:raise Exception: depends on the connected callable.
		"""
		
		if self.__connection is None:
			return
		
		callback = unweak(self.__connection)

		if (self.__flags & SINGLE_ONE_SHOT) != 0:
			self.__connection = None

		callback(*args, **kwargs)

	__call__ = emit

	def copy(self) -> Single[P]:
		""" creates a new instance of this object with a copy of the current connection. """

		return Single(unweak(self.__connection) \
			if not self.__connection is None else None, self.__flags)

	__copy__ = copy

class Queue[**P]:
	""" object that store an ordered collection of callables and emittion will call the oldest
	callable avaiable.
	"""

	def __init__(self):
		self.__connections: list[tuple[CallbackType[P, Any], bool]] = []

	def __weakconnect_dead__(self, ref: WeakMethod[Callable[P, Any]]) -> None:

		del self.__connections[next((idx for (idx, c) \
			in enumerate(self.__connections) if c == ref))]

	def __connect__(self, callback: Callable[P, Any], noweak: bool) -> tuple[CallbackType[P, Any], bool]:

		return (weakify(callback, self.__weakconnect_dead__) \
			if not noweak else callback, noweak, )

	def connect(self, callback: Callable[P, Any], *, noweak: bool = False) -> None:
		""" appends a new connection to this queue.

		by default a connection may use a weak reference to the callable if it's an object method
		and automatically disconnects when the object is destroyed from memory.
		
		:param noweak: if enabled will always use a reference of the callable and keeps the object alive.
		"""

		self.__connections.append(self.__connect__(callback, noweak))

	def connect_all(self, *callbacks: Callable[P, Any], noweak: bool = False) -> None:
		""" same as :func:`connect` will connect each callable at once. """

		self.__connections.extend(map(lambda c: self.__connect__(c, noweak), callbacks))

	def disconnect(self, callback: Callable[P, Any]) -> None:
		""" disconnects all connections of a callable from this queue.
		
		will do nothing if the callable wasn't connected.
		"""

		self.__connections[:] = filter(lambda c: unweak(c[0]) == callback, self.__connections)

	def disconnect_each(self, *callbacks: Callable[P, Any]) -> None:
		""" same as :func:`disconnect` but disconnects multiple callbacks at once. """

		self.__connections[:] = filter(lambda c: unweak(c[0]) in callbacks, self.__connections)

	def disconnect_all(self) -> None:
		""" disconnects all callables from this queue immediatly. """

		self.__connections.clear()

	def is_connected(self, callback: Callable[P, Any]) -> bool:
		""" checks if the callable has at least one connection in this queue. """

		return not next((c for c in self.__connections \
			if unweak(c[0]) == callback), None) is None

	__contains__ = is_connected

	def emit(self, *args: P.args, **kwargs: P.kwargs) -> bool:
		""" calls the oldest callable from the queue avaiable with the argouments is do nothing if
		none are avaiable.

		returns `True` if a callable has been called otherwise `False` if the queue has called all
		avaiable callables.

		will raise any exception thrown by the callable.

		:raise Exception: depends on the connected callable.
		:returns: if a callable was avaiable and has been emitted.
		"""

		if len(self.__connections) == 0:
			return False

		(unweak(self.__connections.pop(0)[0]))(*args, **kwargs)
		return True

	__call__ = emit

	def extend(self, other: Queue[P]) -> None:
		""" copies and appends each connections from another queue into this one. """

		self.__connections.extend(\
			map(lambda c: self.__connect__(unweak(c[0]), c[1]), other.__connections))

	def copy(self) -> Queue[P]:
		""" creates a new queue with a copy of all connections from this queue. """

		queue: Queue[P] = Queue()
		queue.__connections.extend(\
			map(lambda c: self.__connect__(unweak(c[0]), c[1]), self.__connections))

		return queue

	__copy__ = copy

SIGNAL_NO_WEAK: int = 1
""" always use a reference to the callable object. """
SIGNAL_ONE_SHOT: int = 2
""" disconnects the callable before being emitted. """
SIGNAL_MULTI_CONNECT: int = 4
""" allows the same callable to be connected again to the signal. """
SIGNAL_INTERRUPT_EXCEPTION: int = 8
""" interrupts emittion if the callable raises any exception. """

class Signal[**P]:
	""" objects that store an ordered collection of callables and emittion will call each callables
	sequencially.
	"""

	def __init__(self) -> None:
		self.__connections: list[tuple[CallbackType[P, Any], int]] = []

	def __weakconnect_dead__(self, ref: WeakMethod[Callable[P, Any]]) -> None:

		self.__connections[:] = filter(lambda c: c[0] == ref, self.__connections)

	def __connect__(self, callback: Callable[P, Any], flags: int = 0) -> tuple[CallbackType[P, Any], int]:

		return (weakify(callback, self.__weakconnect_dead__) \
			if (flags & SIGNAL_NO_WEAK) != 0 else callback, flags, )

	def connect(self, callback: Callable[P, Any], flags: int = 0) -> None:
		""" append a new connection. won't connect if it fails.

		:raise AlreadyConnectedException: if the :const:`SIGNAL_MULTI_CONNECT` isn't enabled and
			the callable is already connected.
		"""

		if (flags & SIGNAL_MULTI_CONNECT) == 0 \
			and not next((c for c in self.__connections if unweak(c[0]) == callback), None) is None:

			raise AlreadyConnectedException()
		
		self.__connections.append(self.__connect__(callback, flags))

	def connect_all(self, *callbacks: Callable[P, Any], flags: int = 0) -> None:
		""" same as :func:`connect` but connects multiple callables at once with the same flags.
		won't connect anything if at least one of the callable fails connection.

		:raise AlreadyConnectedException: on the first callable that's already connected whitout
			using the :const:`SIGNAL_MULTI_CONNECT` flag.
		"""

		if (flags & SIGNAL_MULTI_CONNECT) == 0 \
			and not next(filter(lambda c: unweak(c[0]) in callbacks, self.__connections), None) is None:

			raise AlreadyConnectedException()

		self.__connections.extend(map(self.__connect__, callbacks))

	def disconnect(self, callback: Callable[P, Any]) -> None:
		""" removes any connection (if multiple exists) of a callable from this signal. won't do
		anything if the callable isn't connected.
		"""

		self.__connections[:] = filter(lambda c: unweak(c[0]) == callback, self.__connections)

	def disconnect_each(self, *callbacks: Callable[P, Any]) -> None:
		""" same as :func:`disconnect` but disconnects multiple callbacks at once. """

		self.__connections[:] = filter(lambda c: unweak(c[0]) in callbacks, self.__connections)

	def disconnect_all(self) -> None:
		""" disconnects all callables immediatly. """

		self.__connections.clear()

	def is_connected(self, callback: Callable[P, Any]) -> bool:
		""" checks if the callable has at least connection in this signal. """

		return not next((c for c in self.__connections \
			if unweak(c[0]) == callback), None) is None
	
	__contains__ = is_connected

	def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
		""" calls each connected callable sequencially ordered by the oldest.

		will raise an exception group for all exceptiong captured from the callables.

		before being called the callable will be disconnected if :const:`SIGNAL_ONE_SHOT` has
		been used.
		
		by default an exception won't interrupt the call sequence but if the callable has been
		connected with the :const:`SIGNAL_INTERRUPT_EXCEPTION` will interrupt the call sequence.

		:raises ExceptionGroup: any exception raised by the callables.
		"""
		
		exceptions: list[Exception] = []
		idx: int = 0

		while idx != len(self.__connections):

			entry = self.__connections[idx]
			(connection, flags, ) = entry

			if (flags & SIGNAL_ONE_SHOT) == 0:
				idx += 1
			else:
				del self.__connections[idx]
			
			try:
				unweak(connection)(*args, **kwargs)
			except Exception as e:
				exceptions.append(e)

				if (flags & SIGNAL_INTERRUPT_EXCEPTION) != 0:
					break
					
		if len(exceptions) != 0:
			raise ExceptionGroup("Exception(s) were raised while signal emittion.", exceptions)

	__call__ = emit

	def extend(self, other: Signal[P]) -> None:
		""" appends all connections from another signal into this one using their original flags.
		
		will raise an exception and won't connect anything if at least one connection already exist
		in this signal whitout using the :const:`SIGNAL_MULTI_CONNECT` flag.
		"""

		callbacks = map(lambda c: unweak(c[0]), other.__connections)

		if not next(filter(lambda c: (c[1] & SIGNAL_MULTI_CONNECT) == 0 \
			and unweak(c[0]) in callbacks, self.__connections), None) is None:
			# finds if there's at least one callback already connected in this signal that doesn't
			# use the multi connect flag. just like in connect this should fail.

			raise AlreadyConnectedException()

		# NOTE (23 apr 2025) Gianpiero Maggiulli
		#  rebuilds each weak reference using this signal. despite those could be simply be copied
		#  from the other signal. could that speed up things? But won't allow this signal to call
		#  his own connect method.

		connections = map(lambda entry: \
			self.__connect__(entry[1], other.__connections[entry[0]][1]), enumerate(callbacks))
		
		self.__connections.extend(connections)

	def copy(self) -> Signal[P]:
		""" creates a new signal with a copy of all connections. """

		signal: Signal[P] = Signal()
		connections = map(lambda c: (weakify(unweak(c[0]), signal.__weakconnect_dead__), c[1], ), self.__connections)

		signal.__connections.extend(connections)

		return signal
	
	__copy__ = copy

	def __deepcopy__(self, *_) -> Signal[P]:
		return self.copy()

__all__ = ('AlreadyConnectedException',
	'Single', 'Signal', 'Queue',
	'SINGLE_NO_WEAK', 'SINGLE_ONE_SHOT',
	'SIGNAL_NO_WEAK', 'SIGNAL_ONE_SHOT', 'SIGNAL_MULTI_CONNECT', 'SIGNAL_INTERRUPT_EXCEPTION', )
