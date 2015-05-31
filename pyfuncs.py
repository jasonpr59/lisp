import operator

import datatypes

def _add(args):
    return sum(args)

def _mul(args):
    return reduce(operator.mul, args)

def _car(args):
    assert len(args) == 1
    pair = args[0]
    assert isinstance(pair, datatypes.Pair)
    return pair.car

def _cdr(args):
    assert len(args) == 1
    pair = args[0]
    assert isinstance(pair, datatypes.Pair)
    return pair.cdr

def _cons(args):
    assert len(args) == 2
    return datatypes.Pair(args[0], args[1])

def _make_list(args):
    result = datatypes.null
    for element in reversed(args):
        result = _cons([element, result])
    return result

functions = {
    '+': _add,
    '*': _mul,
    'list': _make_list,
    'cons': _cons,
    'car': _car,
    'cdr': _cdr,
}
