from emitcallback import Signal, Single, Queue

def callback(value: int) -> None:
	print(f"Value is {value} !")

# put list of argouments type you expect separated by commas.
s1 = Signal[int]()

# type hints will show a warning if the callback doesn't match his signature
# or if emit doesn't have all argouments.
s1.connect(callback)
s1.emit(10)
