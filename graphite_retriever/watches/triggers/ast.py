from .util import recordtype


Variable = recordtype('Variable', 'name')
Number = recordtype('Number', 'value')
MethodCall = recordtype('MethodCall', 'name', 'parameters')
BinaryExpression = recordtype('BinaryExpression', 'left', 'op', 'right')


def method_call_repr(self):
    params = ", ".join([repr(p) for p in self.parameters])
    return '{{MethodCall: {}({})}}'.format(self.name, params)


Variable.__repr__ = lambda self: '{{Variable: {}}}'.format(self.name)
Number.__repr__ = lambda self: '{{Number: {}}}'.format(self.value)
MethodCall.__repr__ = method_call_repr
BinaryExpression.__repr__ = lambda self: '{{Binary: {} {} {}}}'.format(self.left, self.op, self.right)
