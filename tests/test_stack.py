import pytest
from datastructures.stack import Stack, StackUnderflow, StackOverflow

def test_push_pop_peek():
    s = Stack()
    s.push(1); s.push(2)
    assert len(s) == 2
    assert s.peek() == 2
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()

def test_underflow_on_pop():
    s = Stack()
    with pytest.raises(StackUnderflow):
        s.pop()

def test_underflow_on_peek():
    s = Stack()
    with pytest.raises(StackUnderflow):
        s.peek()

def test_overflow_when_maxlen_exceeded():
    s = Stack(maxlen=2)
    s.push("a"); s.push("b")
    with pytest.raises(StackOverflow):
        s.push("c")

def test_clear():
    s = Stack()
    s.push(10); s.push(20)
    s.clear()
    assert s.is_empty()
