from collections import defaultdict

def dump(tests, mocks):
  getFilename = lambda code: code.co_filename.split('/')[-1]
  getLineno = lambda code: code.co_firstlineno
  getLocation = lambda code: '%s:%s' % (getFilename(code), getLineno(code))
  getTestname = lambda filename: filename.replace('.py','').capitalize() + 'Test'
  getObjectId = lambda obj: '%s:%s' % (type(obj).__name__, id(obj))
  getModname = lambda filename: filename.replace('.py','')
  isObject = lambda obj: isinstance(obj, object) and not isinstance(obj, str)
  getAssert = lambda value: 'IsInstance' if isObject(value) else 'Equals'
  getAssertValue = lambda value: type(value).__name__ if isObject(value) else repr(value)

  imports = set(['import unittest', 'from unittest.mock import patch'])
  files = defaultdict(list)
  for code,function in tests.items():
    files[getFilename(code)].append((code,function))

  output = []
  for filename,functions in files.items():
    output.append('')
    output.append('')
    output.append('class %s(unittest.TestCase):' % getTestname(filename))
    instances = {}
    for code,function in sorted(functions, key=lambda fn: fn[0].co_name):
      if code.co_name == '__init__':
        for _,calls in function.calls.items():
          for (args,returnValue) in calls:
            self = args['self']
            imports.add('from %s import %s' % (
              getModname(filename), type(self).__name__)
            )
            del args['self']
            instances[getObjectId(self)] = (type(self).__name__, args)
      else:
        mockArgs = ''
        uniqueMocks = set((c.co_name,m) for c,m in function.mocks)
        for (mockCode,mock) in uniqueMocks:
          args,returnValue = list(mock.calls.values())[0][0]
          self = args.get('self')
          output.append('  @patch.object(%s, \'%s\')' % (
              type(self).__name__, mockCode
          ))
          mockArgs += ', mock_%s' % mockCode
        output.append('  def test_%s(self%s):' % (code.co_name, mockArgs))
        for (mockCode,mock) in uniqueMocks:
          args,returnValue = list(mock.calls.values())[0][0]
          output.append('    mock_%s.return_value = %s' % (
              mockCode, repr(returnValue))
          )
        for (_,calls) in list(function.calls.items())[:1]:
          for (args,returnValue) in calls[:1]:
            self = args.get('self')
            if self:
              typename, initArgs = instances[getObjectId(self)]
              imports.add('import %s' % getModname(filename))
              output.append('    _%s = %s(%s)' % (
                typename.lower(),
                typename,
                ','.join(['%s=%s' % (k,repr(v)) for k,v in initArgs.items()])
              ))
              del args['self']
              output.append('    self.assert%s(_%s.%s(%s), %s)' % (
                getAssert(returnValue),
                typename.lower(),
                code.co_name,
                ','.join(['%s=%s' % (k,repr(v)) for k,v in args.items()]),
                getAssertValue(returnValue)
              ))
            else:
              output.append('    self.assert%s(%s.%s(%s), %s)' % (
                getAssert(returnValue),
                getModname(filename),
                code.co_name,
                ','.join(['%s=%s' % (k,repr(v)) for k,v in args.items()]),
                getAssertValue(returnValue)
              ))
            output.append('')

    output.append('if __name__ == "__main__":')
    output.append('  unittest.main()')

  output = sorted(imports) + output
    
  return '\n'.join(output)
