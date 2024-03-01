from common.base import Base

class Stack:
  def __init__(self) -> None:
    self.stack = []

  def push(self, item):
    self.stack.append(item)

  def pop(self):
    if len(self.stack) is 0:
      Base.error("stack is empty, can't pop any item")
    return self.stack.pop()
  
  def top(self):
    if len(self.stack) is 0:
      Base.error("stack is empty, there is no item at the top of stack")
    return self.stack[-1]
  
  def clean(self):
    self.stack = []

  def show(self):
    Base.print(self.stack)