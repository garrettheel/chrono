import token
import operator as op

from funcparserlib.lexer import Token
from funcparserlib.parser import (some, a, maybe, finished, skip, many, oneplus, forward_decl)


class Token(object):
    def __init__(self, code, value, start=(0, 0), stop=(0, 0), line=''):
        self.code = code
        self.value = value
        self.start = start
        self.stop = stop
        self.line = line

    @property
    def type(self):
        return token.tok_name[self.code]

    def __unicode__(self):
        pos = '-'.join('%d,%d' % x for x in [self.start, self.stop])
        return "%s %s '%s'" % (pos, self.type, self.value)

    def __repr__(self):
        return 'Token(%r, %r, %r, %r, %r)' % (
            self.code, self.value, self.start, self.stop, self.line)

    def __eq__(self, other):
        return (self.code, self.value) == (other.code, other.value)


def recordtype(typename, *fields):

    def init(self, *args):
        if len(args) != len(fields):
            print typename, len(args), len(fields), fields
            raise ValueError()
        for i, f in enumerate(fields):
            setattr(self, f, args[i])

    def repr(self):
        return "<{}>".format(typename)

    Clazz = type(typename, (), {
        '__init__': init,
        '__repr__': repr
    })

    return Clazz


unarg = lambda f: lambda x: f(*x)

@unarg
def eval_expr(z, list):
    return reduce(lambda s, (f, x): f(s, x), list, z)

@unarg
def make_list(first, rest):
    if len(rest) == 0:
        return [first]
    else:
        items = list(rest)  # TODO: same as [first] + rest ?
        items.insert(0, first)
        return items

make_maybe_empty_list = lambda arg: [] if arg is None else make_list(arg)

const = lambda x: lambda _: x
tokval = lambda x: x.value
toktype = lambda t: some(lambda x: x.type == t) >> tokval

op = lambda s: a(Token(token.OP, s)) >> tokval
op_ = lambda s: skip(op(s))

comma = op_(',')

openparen = op_('(')
closeparen = op_(')')
inparens = lambda s: openparen + s + closeparen

number = some(lambda tok: tok.code == token.NUMBER) >> tokval >> float
rawname = (some(lambda tok: tok.code == token.NAME) >> tokval)

maybe_empty_listof = lambda s: maybe(s + many(comma + s)) >> make_maybe_empty_list

endmark = a(Token(token.ENDMARKER, ''))
end = skip(endmark + finished)
