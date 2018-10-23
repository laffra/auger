from collections import defaultdict
import sys

PYTHON2 = getattr(sys.version_info, "major", 0) == 2
PYTHON3 = getattr(sys.version_info, "major", 0) == 3

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

def get_code(func):
    if PYTHON2: return getattr(func, "func_code", getattr(getattr(func, "im_func", None), "func_code", None))
    if PYTHON3: return func.__code__
    unsupported()

def get_code_filename(code):
    return code.co_filename

def get_code_name(code):
    return code.co_name

def get_code_lineno(code):
    return code.co_firstlineno

def unsupported():
    raise NotImplementedError("Unsupported Python version %s" % sys.version)
