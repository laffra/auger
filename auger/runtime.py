from collections import defaultdict


class Function(object):
  def __init__(self):
    self.calls = defaultdict(list)
    self.work = []
    self.mocks = []

  def handleCall(self, args):
    self.work.append(args)
      
  def handleReturn(self, args, value):
    callArgs = self.work.pop()
    self.calls[repr(callArgs)].append((callArgs,value))

  def addMock(self, mock):
    self.mocks.append(mock)
