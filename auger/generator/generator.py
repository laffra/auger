from __future__ import print_function
import os
import sys

file_to_module_name = dict()


def init_module_names():
    modules = [item for item in sys.modules.items()]
    file_to_module_name.update(dict(
        (getattr(mod, '__file__').replace('.pyc', '.py'), name)
        for name, mod in modules
        if hasattr(mod, '__file__')
    ))

def get_module_name(filename):
    path = os.path.normpath(filename)
    if not path in file_to_module_name:
        print('Cannot find %s module name in:' % path)
        for k,v in file_to_module_name.items():
            print(k, '=', v)
    return file_to_module_name.get(path, filename)

class Generator(object):
    def __init__(self):
        init_module_names()

    def dump(self, file_name, module, functions):
        pass
