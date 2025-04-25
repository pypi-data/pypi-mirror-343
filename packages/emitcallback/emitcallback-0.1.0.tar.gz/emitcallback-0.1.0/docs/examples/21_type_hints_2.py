from emitcallback import Signal, Single, Queue

# other combinations of type hints:
Signal[int]()
Signal[str, int]()
Signal[int, str, bool]()
Signal[list[int], bool]()

Single[int]()
Single[str, int]()
Single[int, str, bool]()
Single[list[int], bool]()

Queue[int]()
Queue[str, int]()
Queue[int, str, bool]()
Queue[list[int], bool]()

# using it with variables:
s1 = Signal[int]()

s2: Signal[int] = Signal()
