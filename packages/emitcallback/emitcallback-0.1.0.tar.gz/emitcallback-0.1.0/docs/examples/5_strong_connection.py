from emitcallback import Signal, SIGNAL_NO_WEAK

class Class:

	def method(self):
		print("Hello Class!")

# here object is created.
obj = Class()

# here method (using weak reference is connected) is connected.
s = Signal()
s.connect(obj.method, flags = SIGNAL_NO_WEAK)

# garbage collector reduces reference but object has still one left from the signal.
del obj

# calls the method. here the obj variable is no longer avaiable but object still exist.
s.emit()
