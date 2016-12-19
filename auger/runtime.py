from collections import defaultdict


class Function(object):
    def __init__(self):
        self.calls = defaultdict(list)
        self.work = []
        self.mocks = []

    def handle_call(self, code, args):
        self.work.append(args)

    def handle_return(self, code, args, value):
        callArgs = self.work.pop()
        self.calls[repr(callArgs)].append((callArgs, value))

    def add_mock(self, code, function):
        self.mocks.append((code, function))

    def __str__(self):
        return 'Function(%s)' % self.calls
