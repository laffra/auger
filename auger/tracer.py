from __future__ import absolute_import
from __future__ import print_function
import sys

traces = []

class Tracer(object):
    depth = 0
    filename = ''

    def __enter__(self):
        sys.settrace(self.trace)

    def __exit__(self, exception_type, value, tb):
        sys.settrace(None)
        print()
        for line in traces[:-1]:
            print(line)

    def trace(self, frame, event, args):
        filename = frame.f_code.co_filename
        if not filename or not 'auger' in filename:
            return
        lineno = frame.f_lineno
        name = frame.f_code.co_name
        if event == 'call':
            args = ", ".join(["%s = %s" % (key, repr(value)) for key, value in frame.f_locals.items()])
            self.log(filename, lineno, '%s(%s)' % (name, args))
            self.depth += 1
        elif event == 'return':
            self.log(filename, lineno, ' return %s' % repr(args))
            self.depth -= 1
        return self.trace

    def log(self, filename, lineno, message):
        output = ""
        if filename != self.filename:
            self.filename = filename
        output += '%12s:%-6s' % (filename.split("/")[-1], lineno) + ' ' + '  ' * self.depth + ' '
        if message:
            output += message
        traces.append(output)
