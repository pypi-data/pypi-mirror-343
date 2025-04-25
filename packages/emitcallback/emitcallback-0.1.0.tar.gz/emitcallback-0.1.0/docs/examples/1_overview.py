from emitcallback import Single, Signal, Queue

# example method we want to connect.
def callback():
	print("Hello World!")

# create a single and connect the callback.
single = Single()
single.connect(callback)

# create a signal and connect the callback.
signal = Signal()
signal.connect(callback)

# create a queue and connect the callback.
queue = Queue()
queue.connect(callback)
