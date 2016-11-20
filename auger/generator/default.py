from collections import defaultdict
import inspect
import os

from auger.generator.generator import Generator


class DefaultGenerator(Generator):
    def __init__(self):
        self.output_ = []
        self.imports_ = {'import unittest', 'from unittest.mock import patch'}

    def dump(self, file_names, function_calls):
        self.dump_tests(self.group_by_file(file_names, function_calls))
        return '\n'.join(sorted(self.imports_) + self.output_)

    @staticmethod
    def group_by_file(file_names, function_calls):
        files = defaultdict(list)
        for code, function in function_calls.items():
            file_name = os.path.normpath(code.co_filename)
            if file_name in file_names:
                files[file_name].append((code, function))
        return files

    def collect_instances(self, functions):
        instances = {}
        for code, function in filter(lambda fn: fn[0].co_name == '__init__', functions):
            for _, calls in function.calls.items():
                for (args, return_value) in calls:
                    func_self = args['self']
                    # self.imports_.add('from %s import %s' % (
                    #  self.get_modname(filename), type(func_self).__name__)
                    #              )
                    del args['self']
                    instances[self.get_object_id(func_self)] = (type(func_self).__name__, code, args)
        return instances

    @staticmethod
    def get_mocks(function):
        return set((c.co_name, m) for c, m in function.mocks)

    @staticmethod
    def get_mock_args(mocks):
        return ''.join([', mock_%s' % mockCode for (mockCode, mock) in mocks])

    def dump_mock_decorators(self, mocks):
        last_position = len(self.output_)
        for (code, mock) in mocks:
            args, _ = list(mock.calls.values())[0][0]
            func_self = args.get('self')
            self.output_.insert(last_position, '  @patch.object(%s, \'%s\')' % (type(func_self).__name__, code))

    def dump_mock_return_values(self, mocks):
        for (code, mock) in mocks:
            args, return_value = list(mock.calls.values())[0][0]
            self.output_.append('    mock_%s.return_value = %s' % (code, repr(return_value)))

    def dump_create_instance(self, typename, code, init_args):
        args, varargs, kwargs = inspect.getargs(code)
        params = ', '.join(
            [repr(init_args[arg]) for arg in args[1:]] +
            [repr(arg) for arg in init_args[varargs]] +
            ['%s=%s' % (k,repr(v)) for k,v in init_args.get(kwargs,{})]
        )
        self.output_.append('    %s_instance = %s(%s)' % (
            typename.lower(),
            typename,
            params
        ))

    def add_import(self, filename):
        self.imports_.add(self.get_modname(filename))

    def get_instance(self, instances, func_self):
        return instances[self.get_object_id(func_self)]

    def dump_call(self, filename, code, instances, call):
        for (args, return_value) in call:
            func_self = args.get('self')
            if func_self:
                self.add_import(filename)
                typename, init, init_args = self.get_instance(instances, func_self)
                self.dump_create_instance(typename, init, init_args)
                del args['self']
                target = '%s_instance' % typename.lower()
            else:
                target = self.get_modname(DefaultGenerator.shorten_filename(filename))

            self.output_.append('    self.assert%s(%s.%s(%s), %s)' % (
                self.get_assert(return_value),
                target,
                code.co_name,
                ','.join(['%s=%s' % (k, repr(v)) for k, v in args.items()]),
                self.get_assert_value(return_value)
            ))
            self.output_.append('')

    def dump_tests(self, calls_per_file):
        for filename, functions in calls_per_file.items():
            self.output_.append('')
            self.output_.append('')
            self.output_.append('class %s(unittest.TestCase):' % self.get_testname(filename))
            instances = self.collect_instances(functions)
            functions = filter(lambda fn: fn[0].co_name != '__init__', functions)
            functions = sorted(functions, key=lambda fn: fn[0].co_name)
            for code, function in functions:
                mocks = self.get_mocks(function)
                self.dump_mock_decorators(mocks)
                self.output_.append('  def test_%s(self%s):' % (code.co_name, self.get_mock_args(mocks)))
                self.dump_mock_return_values(mocks)
                self.dump_call(filename, code, instances, list(function.calls.values())[0])

            self.output_.append('if __name__ == "__main__":')
            self.output_.append('  unittest.main()')

    @staticmethod
    def get_filename(code):
        return DefaultGenerator.shorten_filename(code.co_filename)

    @staticmethod
    def shorten_filename(filename):
        return filename.split('/')[-1].split('\\')[-1]

    @staticmethod
    def get_lineno(code):
        return code.co_firstlineno

    @staticmethod
    def get_location(code):
        return '%s:%s' % (DefaultGenerator.get_filename(code), DefaultGenerator.get_lineno(code))

    @staticmethod
    def get_testname(filename):
        return DefaultGenerator.shorten_filename(filename).replace('.py', '').capitalize() + 'Test'

    @staticmethod
    def get_object_id(obj):
        return '%s:%s' % (type(obj).__name__, id(obj))

    @staticmethod
    def get_modname(filename):
        return filename.replace('.py', '')

    @staticmethod
    def is_object(obj):
        return isinstance(obj, object) and not isinstance(obj, str)

    @staticmethod
    def get_assert(value):
        return 'IsInstance' if DefaultGenerator.is_object(value) else 'Equals'

    @staticmethod
    def get_assert_value(value):
        return type(value).__name__ if DefaultGenerator.is_object(value) else repr(value)

