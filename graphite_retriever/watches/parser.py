import re
import six
import logging
import itertools
import operator as op

from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import (some, a, maybe, finished, skip, many, oneplus, forward_decl)


logger = logging.getLogger(__name__)


COMPARATORS = {'>': op.gt, '>=': op.ge, '<': op.lt, '<=': op.le, '==': op.eq, '!=': op.ne}
OPERATORS = {'*': op.mul, '/': op.truediv, '+': op.add, '-': op.sub}
LOGICAL_OPERATORS = {'AND': op.and_, 'OR': op.or_}


TRIGGER_TOKENIZER = make_tokenizer(
    [
        ('Comparator', (r'({0})'.format('|'.join(sorted(COMPARATORS.keys(), reverse=True))),)),
        ('LogicalOperator', (r'({0})'.format('|'.join(map(re.escape, LOGICAL_OPERATORS.keys()))),)),
        ('Operator', (r'(?:\*|\+|-|\/)',)),
        ('Number', (r'(\d+\.?\d*)',)),
        ('Variable', (r'[a-zA-Z_][a-zA-Z_0-9]*',)),
        ('Space', (r'\s+',))
    ]
)


class UnresolvedVariableError(ValueError):
    pass


# TODO: figure out the naming of these
class Expr(object):
    """ An expression which resolves to a value.
    """
    def __init__(self, *parts):
        self.parts = parts
        
    def __repr__(self):
        return "<Expr: {}>".format(' '.join(map(repr, self.parts)))

    def evaluate(self, variables=None):
        variables = variables or {}
        parts = list(self.parts)
        value_range = xrange(0, len(parts), 2)
        
        # Set variables
        for i in value_range:
            var_name = parts[i]
            if not isinstance(var_name, six.string_types):
                continue
            if var_name in variables:
                parts[i] = variables[var_name]
            else:
                raise UnresolvedVariableError("Unresolved variable: {}".format(var_name))

        self._evaluate_ops(parts, OPERATORS.get('*'), OPERATORS.get('/'))
        self._evaluate_ops(parts, OPERATORS.get('+'), OPERATORS.get('-'))

        assert len(parts) == 1, "There should only be one value remaining"
        return parts[0]


    def _evaluate_ops(self, parts, *ops):
        ops_remaining = True
        while ops_remaining:
            if len(parts) <= 1:
                break
            value_range = range(0, len(parts), 2)[:-1]
            for i in value_range:
                if parts[i+1] in ops:
                    lhs, op, rhs = (parts.pop(i) for _ in range(3))
                    parts.insert(i, op(lhs, rhs))
                    break
                elif i == value_range[-1]:
                    ops_remaining = False


class BoolExpr(object):
    """ An expression which resolves to a boolean.
    """
    def __init__(self, lhs, bool_op, rhs):
        self.lhs = lhs
        self.bool_op = bool_op
        self.rhs = rhs

    def __repr__(self):
        return '<BoolExpr: {} {} {}>'.format(self.lhs, self.bool_op, self.rhs)
        
    def evaluate(self, variables=None):
        variables = variables or {}
        return self.bool_op(self.lhs.evaluate(variables),
                            self.rhs.evaluate(variables))


class Trigger(object):
    def __init__(self, *bool_exprs):
        assert len(bool_exprs) >= 1
        self.bool_exprs = bool_exprs

    def evaluate(self, variables=None):
        variables = variables or {}
        results = list(self.bool_exprs)

        # evaluate all exprs
        for i in xrange(0, len(self.bool_exprs), 2):
            results[i] = results[i].evaluate(variables)

        while len(results) > 1:
            lhs, op, rhs = (results.pop(0) for _ in range(3))
            results.insert(0, op(lhs, rhs))

        return results[0]


def tokenize(_str):
    return [x for x in TRIGGER_TOKENIZER(_str) if x.type not in ['Space']]


def parse(seq):
    make_expr = lambda x: Expr(*[x[0]] + list(itertools.chain.from_iterable(x[1])))
    make_bool_expr = lambda x: BoolExpr(*x)
    make_trigger = lambda x: Trigger(*[x[0]] + list(itertools.chain.from_iterable(x[1])))
    
    tokval = lambda x: x.value
    toktype = lambda t: some(lambda x: x.type == t) >> tokval
    sep = lambda s: a(Token(u'Sep', s)) >> tokval
    s_sep = lambda s: skip(sep(s))

    comparator = toktype('Comparator') >> COMPARATORS.get
    number = toktype('Number') >> float
    variable = toktype('Variable')
    operator = toktype('Operator') >> OPERATORS.get
    logical_operator = toktype('LogicalOperator') >> LOGICAL_OPERATORS.get
    value = number | variable
        
    exp = value + many(operator + value) >> make_expr
    bool_exp = exp + comparator + exp >> make_bool_expr
    trigger = bool_exp + many(logical_operator + bool_exp) >> make_trigger

    overall = trigger + skip(finished)
    return overall.parse(seq)


def build_trigger(watch):
    tokens = tokenize(watch)
    r = parse(tokens)
    return r
