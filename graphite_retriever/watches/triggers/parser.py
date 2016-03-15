import re
import six
import token
import logging
import itertools

from funcparserlib.lexer import make_tokenizer
from funcparserlib.parser import (some, a, maybe, finished, skip, many, oneplus, forward_decl)

from .util import const, eval_expr, op, op_, inparens, number, rawname, end, \
                  maybe_empty_listof, unarg, Token
from .ast import Variable, Number, MethodCall, BinaryExpression
from StringIO import StringIO
from tokenize import generate_tokens, NL


logger = logging.getLogger(__name__)


def tokenize(s):
    return list(Token(*t)
        for t in generate_tokens(StringIO(s).readline)
        if t[0] not in [NL, token.NEWLINE])


def parse(tokens):
    makeop = lambda s: op(s) >> const(lambda l, r: BinaryExpression(l, s, r))

    num = number >> Number
    var = rawname >> Variable

    add, sub, mul, div = map(makeop, ['+', '-', '*', '/'])
    lt, lte, gt, gte = map(makeop, ['<', '<=', '>', '>='])

    method_call = forward_decl()
    atom = num | method_call | var

    expr1 = atom + many((mul | div) + atom) >> eval_expr
    expr2 = expr1 + many((add | sub) + expr1) >> eval_expr
    expr3 = expr2 + many((lt | lte | gt | gte) + expr2) >> eval_expr

    method_call.define(rawname + inparens(maybe_empty_listof(expr2)) >> unarg(MethodCall))

    defn = expr3 + end
    return defn.parse(tokens)
