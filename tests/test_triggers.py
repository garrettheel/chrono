import operator as op
from nose.tools import assert_equals, assert_true, assert_false

from graphite_retriever.watches.parser import build_trigger, Expr


def test_evaluate_trigger():
    assert_true(build_trigger("1 < 2").evaluate({}))
    assert_false(build_trigger("1 > 2").evaluate({}))
    
    assert_true(build_trigger("1 < a").evaluate({'a': 2}))
    assert_false(build_trigger("1 > a").evaluate({'a': 2}))
    
    assert_true(build_trigger("1 + 3 * 2 < a AND 2 > 1").evaluate({'a': 8}))


def test_expr():
    assert_equals(Expr(1).evaluate(), 1)
    assert_equals(Expr(1, op.add, 2).evaluate(), 3)
    assert_equals(Expr(1, op.add, 2, op.mul, 3).evaluate(), 7)
    assert_equals(Expr(1, op.add, "a").evaluate({'a': 5}), 6)
    assert_equals(Expr("a", op.mul, "b").evaluate({'a': 5, 'b': 3}), 15)
    assert_equals(Expr("a", op.add, "b", op.mul, 5).evaluate({'a': 2, 'b': 4}), 22)
