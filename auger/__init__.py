import inspect
import sys
import traceback

from collections import defaultdict

from . import runtime
from . import generator

class UnittestGenerator(object):
  _filenames = {}
  _calls = defaultdict(runtime.Function)
  _mocks = defaultdict(runtime.Function)

  def __init__(self, *mods):
    self._filenames = [
	mod.__file__.replace('.pyc', '.py')
	for mod in mods
    ]

  def _getFunction(self, code, isMock):
    return (self._mocks if isMock else self._calls)[code]

  def _handle_call(self, code, locals, args, caller):
    function = self._getFunction(code, caller)
    if caller:
      self._calls[caller].addMock((code,function))
    function.handleCall(locals)
  
  def _handle_return(self, code, locals, args, caller):
    self._getFunction(code, caller).handleReturn(locals, args)
  
  def _handle_line(self, code, locals, args, caller):
    pass
  
  def _handle_exception(self, code, locals, args, caller):
    pass
  
  def __enter__(self):
    sys.settrace(self._trace)

  def __exit__(self, type, value, tb):
    sys.settrace(None)
    print(generator.default.dump(self._calls, self._mocks))

  def _trace(self, frame, event, args):
    handler = getattr(self, '_handle_' + event)
    top = frame.f_code.co_filename
    caller = frame.f_back.f_code.co_filename
    if top in self._filenames:
      handler(frame.f_code, frame.f_locals, args, None)
    if caller in self._filenames and top != caller:
      handler(frame.f_code, frame.f_locals, args, frame.f_back.f_code)

    return self._trace
