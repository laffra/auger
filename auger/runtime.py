from collections import defaultdict


class Function(object):
  def __init__(self):
    self.calls = defaultdict(list)
    self.work = []
    self.mocks = []

  def handle_call(self, args):
    self.work.append(args)
      
  def handle_return(self, args, value):
    callArgs = self.work.pop()
    self.calls[repr(callArgs)].append((callArgs,value))

  def add_mock(self, mock):
    self.mocks.append(mock)
