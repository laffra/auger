import inspect
import random
import sys
import traceback
import types

from auger.generator.generator import Generator
from auger.generator.generator import get_module_name


def indent(n):
    return '    ' * n


class DefaultGenerator(Generator):
    def __init__(self):
        Generator.__init__(self)
        self.output_ = []
        self.imports_ = set([('unittest',)])
        self.instances = {}

    def dump(self, filename, functions):
        self.output_ = []
        self.dump_tests(filename, functions)
        for line in open(filename):
            line = line.replace('\n', '')
            if line.startswith('import '):
                self.imports_.add((line.replace('import ', ''),))
            if line.startswith('from '):
                self.imports_.add(tuple(line.replace('from ', '').replace('import ','').split(' ')))
        return '\n'.join(self.format_imports() + self.output_)

    def format_imports(self):
        imports = sorted(self.imports_)
        def format(imp):
            if len(imp) == 2 and imp[0] != '__main__':
                return 'from %s import %s' % imp
            return 'import %s' % imp[0]
        return map(format, imports)

    def collect_instances(self, functions):
        for code, function in filter(lambda fn: fn[0].co_name == '__init__', functions):
            for _, calls in function.calls.items():
                for (args, _) in calls[:1]:
                    func_self = args['self']
                    func_self_type = func_self.__class__
                    for base in func_self.__class__.__bases__:
                        for _, init in filter(lambda member: member[0] == '__init__', inspect.getmembers(base)):
                            if getattr(init, "__code__", None) == code:
                                func_self_type = base
                    mod = func_self_type.__module__
                    self.imports_.add((mod, func_self_type.__name__))
                    self.instances[self.get_object_id(type(func_self), func_self)] = (func_self_type.__name__, code, args)

    @staticmethod
    def get_mocks(function):
        return set(function.mocks)

    @staticmethod
    def get_mock_args(mocks):
        return ''.join([', mock_%s' % code.co_name for (code, mock) in mocks])

    def find_module(self, code):
        for modname, mod in sys.modules.items():
            file = getattr(mod, '__file__', '').replace('.pyc', '.py')
            if file == code.co_filename:
                if modname == "__main__":
                    modname = file.replace(".py", "").replace("/", ".")
                self.imports_.add((modname,))
                return modname, mod

    def get_defining_item(self, code):
        modname, mod = self.find_module(code)
        for _,clazz in inspect.getmembers(mod, predicate=inspect.isclass):
            for _,member in inspect.getmembers(clazz, predicate=inspect.ismethod):
                filename = member.im_func.func_code.co_filename
                lineno = member.im_func.func_code.co_firstlineno
                if filename == code.co_filename and lineno == code.co_firstlineno:
                    self.imports_.add((modname, clazz.__name__))
                    return clazz, member
            for _,member in inspect.getmembers(clazz, predicate=lambda member: isinstance(member, property)):
                self.imports_.add((modname, clazz.__name__))
                return clazz, member
            for _,member in inspect.getmembers(clazz, predicate=inspect.isfunction):
                filename = member.func_code.co_filename
                lineno = member.func_code.co_firstlineno
                if filename == code.co_filename and lineno == code.co_firstlineno:
                    self.imports_.add((modname, clazz.__name__))
                    return clazz, member
        if modname != '__main__':
            self.imports_.add((modname,))
        return mod, mod

    def dump_mock_decorators(self, mocks):
        last_position = len(self.output_)
        for (code, mock) in mocks:
            definer, member = self.get_defining_item(code)
            self.imports_.add(('mock', 'patch'))
            self.output_.insert(last_position, indent(1) + '@patch.object(%s, \'%s\')' % (
                definer.__name__, code.co_name))

    def dump_mock_return_values(self, mocks):
        for (code, mock) in mocks:
            args, return_value = list(mock.calls.values())[0][0]
            if not self.is_object(return_value):
                return_value = repr(return_value)
            else:
                instance = self.get_instance(self.instances, return_value)
                if instance:
                    return_value = self.get_initializer(*instance)
                else:
                    return_value = "None # TODO: fix mock for %s()" % return_value
            self.output_.append(indent(2) + 'mock_%s.return_value = %s' % (code.co_name, return_value))

    def dump_create_instance(self, typename, code, init_args):
        self.output_.append(indent(2) + '%s_instance = %s' % (typename.lower(), self.get_initializer(typename, code, init_args)))

    def get_initializer(self, typename, code=None, init_args=None):
        if code and init_args:
            args, varargs, kwargs = inspect.getargs(code)
            params = ', '.join(
                [repr(init_args[arg]) for arg in args[1:]] +
                [repr(arg) for arg in init_args.get(varargs, [])] +
                ['%s=%s' % (k, repr(v)) for k, v in init_args.get(kwargs, {})]
            )
        else:
            params = ""
        return '%s(%s)' % (typename, params)

    def add_import(self, filename):
        self.imports_.add((self.get_modname(filename),))

    def get_instance(self, instances, func_self):
        _type = type(func_self)
        return instances.get(self.get_object_id(_type, func_self)) or (func_self.__class__.__name__, _type, {})

    def dump_call(self, filename, code, call):
        definer, member = self.get_defining_item(code)
        for (args, return_value) in call:
            func_self = args.get('self')
            if isinstance(member, property) or inspect.ismethod(member):
                typename, init, init_args = self.get_instance(self.instances, func_self)
                self.dump_create_instance(typename, init, init_args)
                del args['self']
                target = '%s_instance' % typename.lower()
            else:
                self.add_import(filename)
                target = definer.__name__

            call = '%s.%s' % (target, code.co_name)
            if inspect.ismethod(member):
                call += '(%s)' % (
                    ','.join(['%s=%s' % (k, repr(v)) for k, v in args.items()]),
                )
            call += ',\n'
            self.output_.append(''.join([
                indent(2),
                'self.assert%s(\n' % self.get_assert(return_value),
                indent(3),
                call,
                indent(3),
                '%s\n' % self.get_assert_value(return_value),
                indent(2),
                ')\n'
            ]))
            self.output_.append('')
            break;

    def dump_tests(self, filename, functions):
        self.collect_instances(functions)
        self.output_.append('')
        self.output_.append('')
        self.output_.append('class %s(unittest.TestCase):' % self.get_testname(filename))
        functions = filter(lambda fn: fn[0].co_name != '__init__', functions)
        functions = sorted(functions, key=lambda fn: fn[0].co_name)
        for code, function in functions:
            if function.calls:
                mocks = self.get_mocks(function)
                self.dump_mock_decorators(mocks)
                self.output_.append(indent(1) + 'def test_%s(self%s):' % (code.co_name, self.get_mock_args(mocks)))
                self.dump_mock_return_values(mocks)
                try:
                    self.dump_call(filename, code, random.choice(list(function.calls.values())))
                except:
                    traceback.print_exc()

        self.output_.append('if __name__ == "__main__":')
        self.output_.append(indent(1) + 'unittest.main()\n')

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
    def get_object_id(obj_type, obj):
        return '%s:%s' % (obj_type.__name__, id(obj))

    def get_modname(self, filename):
        return get_module_name(filename)

    @staticmethod
    def is_object(obj):
        return hasattr(obj, '__dict__')

    @staticmethod
    def get_assert(value):
        return 'IsInstance' if DefaultGenerator.is_object(value) else 'Equals'

    @staticmethod
    def get_full_class_name(value):
        return value.__class__.__module__ + "." + value.__class__.__name__

    @staticmethod
    def get_assert_value(value):
        value = DefaultGenerator.get_full_class_name(value) if DefaultGenerator.is_object(value) else repr(value)
        return value.replace("<type '", '').replace("'>", '')


