import operator as op
from nose.tools import assert_equals, assert_true, assert_false, assert_raises

from chrono.watches.triggers import build_trigger
from chrono.watches.triggers.eval import MethodCallError


def test_wrong_number_params():
    with assert_raises(MethodCallError):
        build_trigger("last(t, t) > 0").evaluate({'t': [1]})
    with assert_raises(MethodCallError):
        build_trigger("last(t, t) > 0").evaluate({'t': [1]})


def test_simple_last():
    t = build_trigger("last(t) < 5")

    assert_equals(t.evaluate({'t': [5]}), False)
    assert_equals(t.evaluate({'t': [7,2,5]}), False)
    assert_equals(t.evaluate({'t': [4]}), True)
    assert_equals(t.evaluate({'t': [3,7,2]}), True)


def test_simple_sum():
    t = build_trigger("sum(t) < 5")

    assert_equals(t.evaluate({'t': [3]}), True)
    assert_equals(t.evaluate({'t': [1,1,2]}), True)
    assert_equals(t.evaluate({'t': [6]}), False)
    assert_equals(t.evaluate({'t': [2,1,2,1]}), False)


def test_simple_avg():
    t = build_trigger("avg(t) < 5")

    assert_equals(t.evaluate({'t': [3]}), True)
    assert_equals(t.evaluate({'t': [1,2,3,4,5]}), True)
    assert_equals(t.evaluate({'t': [6]}), False)
    assert_equals(t.evaluate({'t': [4,5,6,7,8]}), False)
