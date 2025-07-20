
class stack:
  def __init__(self):
    self.stack = []

  def push(self, element):
    self.stack.append(element)

  def pop(self):
    if self.empty():
      return "Stack is empty"
    return self.stack.pop()

  def top(self):
    if self.empty():
      return "Stack is empty"
    return self.stack[-1]

  def empty(self):
    return len(self.stack) == 0

  def size(self):
    return len(self.stack)

  def reset(self):
    for item in self.stack: self.pop