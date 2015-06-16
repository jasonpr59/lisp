"""Base functions to be called on Lisp data, implemented in Python."""

import operator

import datatypes

def _add(*args):
    return sum(args)

def _sub(first, *rest):
    # Single-argument _sub is additive inversion.
    # For example, (- 5) is -5.
    if not rest:
        return -first

    return first - sum(rest)

def _mul(*args):
    return reduce(operator.mul, args, 1)

def _div(numerator, *denominators):
    # TODO(jasonpr): Use fractions, not floating point?

    # Single-argument _div is multiplicative inversion.
    # For example, (/ 5) is 1/5.
    if not denominators:
        return 1 / numerator

    result = numerator
    for denom in denominators:
        result /= denom
    return result

def _car(pair):
    assert isinstance(pair, datatypes.Pair)
    return pair.car

def _cdr(pair):
    assert isinstance(pair, datatypes.Pair)
    return pair.cdr

def _cons(car, cdr):
    return datatypes.Pair(car, cdr)

def _list(*elements):
    result = datatypes.null
    for element in reversed(elements):
        result = _cons(element, result)
    return result

def _gt(left, right):
    return datatypes.lisp_bool(left > right)

def _lt(left, right):
    return datatypes.lisp_bool(left < right)

def _ge(left, right):
    return datatypes.lisp_bool(left >= right)

def _le(left, right):
    return datatypes.lisp_bool(left <= right)

def _print(*args):
    for arg in args:
        print arg

def _is_vector(candidate):
    return datatypes.lisp_bool(isinstance(candidate, datatypes.Vector))

# TODO(jasonpr): Figure out a good way to get rid of these
# intermediate functions that check the type and call a method.
def _vector_length(vector):
    assert isinstance(vector, datatypes.Vector)
    return datatypes.Fraction(vector.length())

def _vector_ref(vector, num):
    assert isinstance(vector, datatypes.Vector)
    return vector.get(num)

def _vector_set(vector, num, value):
    assert isinstance(vector, datatypes.Vector)
    vector.set(num, value)

def _vector_fill(vector, fill_value):
    assert isinstance(vector, datatypes.Vector)
    vector.fill(fill_value)

functions = {
    '+': _add,
    '-': _sub,
    '*': _mul,
    '/': _div,
    'list': _list,
    'cons': _cons,
    'car': _car,
    'cdr': _cdr,
    '>': _gt,
    '<': _lt,
    '>=': _ge,
    '<=': _le,
    'print!': _print,
    'vector': lambda *contents: datatypes.Vector(contents),
    'make-vector': lambda *args: datatypes.Vector.make(*args),
    'vector?': _is_vector,
    'vector-length': _vector_length,
    'vector-ref': _vector_ref,
    'vector-set!': _vector_set,
    'vector-fill!': _vector_fill,
}
