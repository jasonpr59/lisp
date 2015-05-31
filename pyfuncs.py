import operator

import datatypes

def _add(args):
    return sum(args)

def _sub(args):
    assert args
    # The result, args[0] - sum(args[1:]), is the same as:
    return 2 * args[0] - sum(args)

def _mul(args):
    return reduce(operator.mul, args, 1)

def _div(args):
    # TODO(jasonpr): Use fractions, not floating point?
    assert args
    # The result, args[0] / prod(args[1:]), is the same as
    # args[0]**2 / prod(args).
    result = args[0] ** 2
    for arg in args:
        result /= arg
    return result

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

def _gt(args):
    assert len(args) == 2
    return args[0] > args [1]

def _lt(args):
    assert len(args) == 2
    return args[0] < args [1]

def _ge(args):
    assert len(args) == 2
    return args[0] >= args [1]

def _le(args):
    assert len(args) == 2
    return args[0] <= args [1]

functions = {
    '+': _add,
    '-': _sub,
    '*': _mul,
    '/': _div,
    'list': _make_list,
    'cons': _cons,
    'car': _car,
    'cdr': _cdr,
    '>': _gt,
    '<': _lt,
    '>=': _ge,
    '<=': _le,
}
