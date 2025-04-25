from emitcallback import Signal, SINGLE_ONE_SHOT, SIGNAL_MULTI_CONNECT

def callback():
	print("Hello World!")

s = Signal()

# allows the function to be connected more than once and that on the next emittion will be disconnected.
s.connect(callback, flags = SINGLE_ONE_SHOT|SIGNAL_MULTI_CONNECT)
s.connect(callback, flags = SIGNAL_MULTI_CONNECT)

# calls both function.
s.emit()
# calls only the one that wasn't connected with oneshot.
s.emit()
