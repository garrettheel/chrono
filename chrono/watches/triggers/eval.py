import re
import inspect
import operator as op

BINARY_OPS = {'*': op.mul, '/': op.truediv, '+': op.add, '-': op.sub, '>': op.gt,
              '>=': op.ge, '<': op.lt, '<=': op.le, '==': op.eq, '!=': op.ne}
LOGICAL_OPS = {'AND': op.and_, 'OR': op.or_}

METHODS = {
    'sum': sum,
    'avg': lambda series: sum(series) / float(len(series)),
    'last': lambda series: series[-1]
}


class Trigger(object):
    def __init__(self, raw, expr):
        self.raw = raw
        self.expr = expr

    def to_json(self):
        return self.raw

    def evaluate(self, ctx={}):
        return self.visit(self.expr, ctx)

    def __repr__(self):
        return self.raw

    def visit(self, node, ctx):
        clz = str(node.__class__.__name__)
        search = re.sub('(?<!^)(?=[A-Z])', '_', clz).lower()  # TODO: could cache this
        visit_node = getattr(self, 'visit_{}'.format(search))
        return visit_node(node, ctx)

    def visit_all(self, nodes, ctx):
        return [self.visit(node, ctx) for node in nodes]

    def visit_variable(self, var, ctx):
        if var.name not in ctx:
            raise UnresolvedVariableError(var.name)
        return ctx.get(var.name)

    def visit_number(self, num, ctx):
        return num.value

    def visit_binary_expression(self, binary_expr, ctx):
        left = self.visit(binary_expr.left, ctx)
        right = self.visit(binary_expr.right, ctx)
        op = BINARY_OPS.get(binary_expr.op)
        return op(left, right)

    def visit_method_call(self, method_call, ctx):
        if method_call.name not in METHODS:
            raise UnknownMethodError(method_call.name)
        param_values = self.visit_all(method_call.parameters, ctx)
        # TODO: error handling for incorrect params

        method = METHODS.get(method_call.name)
        try:
            args, _, _, _ = inspect.getargspec(method)
            if len(args) != len(param_values):
                raise MethodCallError("Incorrect number of params for '{}'. {} != {}"\
                                      .format(method_call.name, len(param_values), len(args)))
        except TypeError:
            pass

        try:
            return METHODS.get(method_call.name)(*param_values)
        except Exception as e:
            raise MethodCallError(e)


class UnresolvedVariableError(ValueError):
    pass


class UnknownMethodError(ValueError):
    pass


class MethodCallError(ValueError):
    pass
