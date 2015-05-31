from collections import namedtuple

class DataType(object):
    pass

class Symbol(DataType):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Symbol(%s)' % self.name


class LispFunction(object):
    def __init__(self, env, arg_names, expr):
        self.env = env
        self.arg_names = arg_names
        self.expr = expr

    def __repr__(self):
        return "LispFunction[%s -> %s]" % (self.arg_names, self.expr)

class Pair(namedtuple('Pair', ['car', 'cdr'])):
    def __repr__(self):
        return '(%s . %s)' % self

class _Null(DataType):
    def __repr__(self):
        return '()'

null = _Null()

def is_null(data):
    return data is null
