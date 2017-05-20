from __future__ import absolute_import

import os
import sys

from collections import defaultdict

from auger import runtime
from auger.generator.default import DefaultGenerator
from auger.generator.generator import get_module_name


class magic(object):
    _file_names = None
    _calls = defaultdict(runtime.Function)

    def __init__(self, modules, generator=None):
        self._file_names = [os.path.normpath(mod.__file__.replace('.pyc', '.py')) for mod in modules]
        self._modules = modules
        self.generator_ = generator or DefaultGenerator()

    def _handle_call(self, code, locals_dict, args, caller=None):
        function = self._calls[code]
        if caller:
            self._calls[caller].add_mock(code, function)
        params = list(code.co_varnames)[:code.co_argcount]
        function.handle_call(code, dict((p,locals_dict[p]) for p in params))

    def _handle_return(self, code, locals_dict, args, caller=None):
        self._calls[code].handle_return(code, locals_dict, args)

    def _handle_line(self, code, locals_dict, args, caller=None):
        pass

    def _handle_exception(self, code, locals_dict, args, caller=None):
        pass

    def __enter__(self):
        sys.settrace(self._trace)

    def __exit__(self, exception_type, value, tb):
        sys.settrace(None)
        subjects = self.group_by_file(self._file_names, self._calls)
        for filename, functions in subjects.items():
            modname = get_module_name(filename)
            root = filename
            for _ in modname.split('.'):
                root = os.path.dirname(root)
            output = os.path.normpath('%s/tests/test_%s.py' % (root, modname.replace('.', '_')))
            with open(output, 'w') as f:
                module = self._modules[self._file_names.index(filename)]
                f.write(self.generator_.dump(filename, module, functions))

    @staticmethod
    def group_by_file(file_names, function_calls):
        file_names = set(file_names)
        files = defaultdict(list)
        for code, function in function_calls.items():
            file_name = os.path.normpath(code.co_filename)
            if file_name in file_names:
                files[file_name].append((code, function))
        return files

    def _trace(self, frame, event, args):
        handler = getattr(self, '_handle_' + event)
        top = frame.f_code.co_filename
        caller = frame.f_back.f_code.co_filename
        if top in self._file_names:
            handler(frame.f_code, frame.f_locals, args)
        if caller in self._file_names and top != caller:
            handler(frame.f_code, frame.f_locals, args, frame.f_back.f_code)

        return self._trace
