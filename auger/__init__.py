from __future__ import absolute_import
from __future__ import print_function

import inspect
import os
import sys
import traceback

from collections import defaultdict

from auger import runtime
from auger.generator.default import DefaultGenerator
from auger.generator.generator import get_module_name


class magic(object):
    _file_names = None
    _caller = "???"
    _calls = defaultdict(runtime.Function)

    def __init__(self, modulesOrClasses, generator=None, verbose=False):
        self._caller = inspect.stack()[1][1]
        self._file_names = map(os.path.normpath, map(self._get_file, modulesOrClasses))
        self.generator_ = generator or DefaultGenerator()
        self.modulesOrClasses = set(modulesOrClasses)
        self.verbose = verbose

    def should_test(self, code):
        for parent in self.modulesOrClasses:
            for _,func in inspect.getmembers(parent, inspect.ismethod):
                if func.im_func.func_code == code:
                    return True
            for _,clazz in inspect.getmembers(parent, inspect.isclass):
                for _,func in inspect.getmembers(clazz, inspect.ismethod):
                    if func.im_func.func_code == code:
                        return True
        return False

    def _get_file(self, moduleOrClass):
        file = self._caller
        try:
            if hasattr(moduleOrClass, "__file__"):
                file = moduleOrClass.__file__
            else:
                file = inspect.getfile(moduleOrClass)
        except:
            pass
        return file.replace('.pyc', '.py')

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
        for filename, functions in self.group_by_file(self._file_names, self._calls).items():
            test = self.generator_.dump(filename, functions)
            if self.verbose:
                print('=' * 47 + ' Auger ' + '=' * 46)
                print(test)
                print('=' * 100)
            else:
                modname = get_module_name(filename)
                if modname == '__main__':
                    modname = filename.replace('.py', '').capitalize();
                root = filename
                for _ in modname.split('.'):
                    root = os.path.dirname(root)
                output = os.path.normpath('%s/tests/test_%s.py' % (root or '.', modname.replace('.', '_')))
                dir = os.path.dirname(output)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(output, 'w') as f:
                    f.write(test)
                print('Auger: generated test: %s' % output)

    def group_by_file(self, file_names, function_calls):
        file_names = set(file_names)
        files = defaultdict(list)
        for code, function in function_calls.items():
            file_name = os.path.normpath(code.co_filename)
            if file_name in file_names and self.should_test(code):
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
