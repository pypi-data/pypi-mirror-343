from emitcallback import Signal

def function():
	print("Hello Function!")

class Class:

	def method(self):
		print("Hello Class!")

obj = Class()

# any connections happens the same way!
s = Signal()
s.connect(lambda: print("Hello Lambda!"))
s.connect(function)
s.connect(obj.method)

s.emit()
