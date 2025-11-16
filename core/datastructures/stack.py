class StackUnderflow(Exception): ...
class StackOverflow(Exception): ...

class Stack:
    def __init__(self, maxlen=None):
        self._data = []
        self._maxlen = maxlen

    def push(self, item):
        if self._maxlen is not None and len(self._data) >= self._maxlen:
            raise StackOverflow("stack is full")
        self._data.append(item)

    def pop(self):
        if not self._data:
            raise StackUnderflow("stack is empty")
        return self._data.pop()

    def peek(self):
        if not self._data:
            raise StackUnderflow("stack is empty")
        return self._data[-1]

    def clear(self):
        self._data.clear()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0
