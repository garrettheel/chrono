from .parser import tokenize, parse
from .eval import Trigger

def build_trigger(raw_trigger):
    tokens = tokenize(raw_trigger)
    root_expr = parse(tokens)
    return Trigger(root_expr)
