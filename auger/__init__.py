import os
import sys

from collections import defaultdict

from auger import runtime
from auger.generator.default import DefaultGenerator


class magic(object):
    _file_names = None
    _calls = defaultdict(runtime.Function)

    def __init__(self, mods, generator=None):
        self._file_names = set(os.path.normpath(mod.__file__.replace('.pyc', '.py')) for mod in mods)
        self.generator_ = generator or DefaultGenerator()

    def _handle_call(self, code, locals_dict, args, caller=None):
        function = self._calls[code]
        if caller:
            self._calls[caller].add_mock((code, function))
        function.handle_call(locals_dict)

    def _handle_return(self, code, locals_dict, args, caller=None):
        self._calls[code].handle_return(locals_dict, args)

    def _handle_line(self, code, locals_dict, args, caller=None):
        pass

    def _handle_exception(self, code, locals_dict, args, caller=None):
        pass

    def __enter__(self):
        sys.settrace(self._trace)

    def __exit__(self, exception_type, value, tb):
        sys.settrace(None)
        print(self.generator_.dump(self._file_names, self._calls))

    def _trace(self, frame, event, args):
        handler = getattr(self, '_handle_' + event)
        top = frame.f_code.co_filename
        caller = frame.f_back.f_code.co_filename
        if top in self._file_names:
            handler(frame.f_code, frame.f_locals, args)
        if caller in self._file_names and top != caller:
            handler(frame.f_code, frame.f_locals, args, frame.f_back.f_code)

        return self._trace
