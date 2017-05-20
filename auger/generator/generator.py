import os
import sys

file_to_module_name = dict()


def init_module_names():
    file_to_module_name.update(dict(
        (getattr(mod, '__file__').replace('.pyc', '.py'), name)
        for name, mod in sys.modules.items()
        if hasattr(mod, '__file__')
    ))

def get_module_name(filename):
    path = os.path.normpath(filename)
    if not path in file_to_module_name:
        print 'Cannot find %s module name in:' % path
        for k,v in file_to_module_name.iteritems():
            print k, '=', v
    return file_to_module_name.get(path, filename)

class Generator(object):
    def __init__(self):
        init_module_names()

    def dump(self, file_name, module, functions):
        pass
