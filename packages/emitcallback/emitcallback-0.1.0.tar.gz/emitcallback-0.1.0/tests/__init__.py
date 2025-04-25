
import emitcallback as evemit

def test_basic() -> None:
	
	s = evemit.Signal[[]]()

	s.connect(lambda: print("Helllo World!"))
	s.emit()
