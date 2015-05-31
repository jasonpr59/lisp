import operator

import datatypes

def add(args):
    return sum(args)

def mul(args):
    return reduce(operator.mul, args)

def car(args):
    assert len(args) == 1
    pair = args[0]
    assert isinstance(pair, datatypes.Pair)
    return pair.car

def cdr(args):
    assert len(args) == 1
    pair = args[0]
    assert isinstance(pair, datatypes.Pair)
    return pair.cdr

def cons(args):
    assert len(args) == 2
    return datatypes.Pair(args[0], args[1])

def make_list(args):
    result = datatypes.null
    for element in reversed(args):
        result = cons([element, result])
    return result
