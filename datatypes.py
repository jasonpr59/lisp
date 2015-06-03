from collections import namedtuple

class DataType(object):
    pass

class Symbol(DataType):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Symbol(%s)' % self.name


class LispFunction(object):
    def __init__(self, env, arg_names, exprs):
        self.env = env
        self.arg_names = arg_names
        self.exprs = exprs

    def __repr__(self):
        return "LispFunction[%s -> %s]" % (self.arg_names, self.exprs)

class Pair(namedtuple('Pair', ['car', 'cdr'])):
    def __repr__(self):
        return '(%s . %s)' % self

class _Boolean(DataType):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return '#t' if self._value else '#f'

_lisp_true = _Boolean(True)
_lisp_false = _Boolean(False)

def lisp_bool(value):
    return _lisp_true if value else _lisp_false


class _Null(DataType):
    def __repr__(self):
        return '()'

null = _Null()

def is_null(data):
    return data is null
