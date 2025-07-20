class Stack:
  def __init__(self):
    self.stack = []

  def push(self, element):
    if(self.size() > 100):
      self.stack.pop(0)
    self.stack.append(element)

  def pop(self):
    if self.empty():
      return None
    return self.stack.pop()

  def top(self):
    if self.empty():
      return None
    return self.stack[-1]

  def empty(self):
    return len(self.stack) == 0

  def size(self):
    return len(self.stack)

  def reset(self):
    self.stack.clear()