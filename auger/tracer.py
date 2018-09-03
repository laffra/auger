from __future__ import absolute_import
from __future__ import print_function

import sys

traces = [];

class Tracer(object):
    depth = 0
    filename = ''

    def __enter__(self):
        sys.settrace(self.trace)

    def __exit__(self, exception_type, value, tb):
        sys.settrace(None)

    def trace(self, frame, event, args):
        filename = frame.f_code.co_filename
        if not filename or not 'auger' in filename:
            return
        lineno = frame.f_lineno
        name = frame.f_code.co_name
        if event == 'call':
            self.log(filename, lineno, '%s(%s)' % (name, str(frame.f_locals)))
            self.depth += 1
        elif event == 'return':
            self.log(filename, lineno, ' => %s' % repr(args))
            self.depth -= 1
        elif event == 'line':
            self.log(filename, lineno, '')
        return self.trace

    def log(self, filename, lineno, message):
        output = ""
        if filename != self.filename:
            output += '\n%s\n' % filename
            self.filename = filename
        with open(filename) as fp:
            line = fp.readlines()[lineno - 1][:-1].strip()
        output += '%06s' % lineno + ' ' + '  ' * self.depth + ' ' + line
        if message:
            output += ' # ' + message
        print(output)
        traces.append(output)
