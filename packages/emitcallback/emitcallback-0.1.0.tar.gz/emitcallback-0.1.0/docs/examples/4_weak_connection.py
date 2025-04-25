from emitcallback import Signal

class Class:

	def method(self):
		print("Hello Class!")

# here object is created.
obj = Class()

# here method (using weak reference is connected) is connected.
s = Signal()
s.connect(obj.method)

# garbage collector destroy the object because there are no more references of it.
# emittion won't call method because it got disconnected here.
del obj

s.emit()
