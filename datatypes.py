from collections import namedtuple

class DataType(object):
    """ABC for Lisp Datatypes.

    We do not guarantee that all Lisp data inherrits from DataType.
    In particular, some Lisp data is simply represented by a basic
    Python type, like int.
    """


class Symbol(DataType):
    """A Scheme symbol equivalent.

    TODO(jasonpr): Justify the existence of symbols in this language.
    """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Symbol(%s)' % self.name


class LispFunction(DataType):
    """A function defined in Lisp."""
    def __init__(self, env, arg_names, exprs):
        self.env = env
        self.arg_names = arg_names
        self.exprs = exprs

    def __repr__(self):
        return "LispFunction[%s -> %s]" % (self.arg_names, self.exprs)

class Pair(namedtuple('Pair', ['car', 'cdr'])):
    """A Lisp pair, with a car and a cdr."""
    def __repr__(self):
        return '(%s . %s)' % self

class Vector(DataType):
    """A collection with O(1) access of any element. """
    def __init__(self, elements):
        self._elements = elements

    def get(self, num):
        return self._elements[num]

    def set(self, num, value):
        # TODO(jasonpr): Determine when to allow vector mutation.
        self._elements[num] = value

    @classmethod
    def make(cls, length, fill_value=0):
        backing_list = [fill_value] * length
        return cls(backing_list)

    def length(self):
        return len(self._elements)

    def as_list(self):
        # TODO(jasonpr): Implement once we've reconciled Python lists
        # with Lisp lists.
        raise NotImplementedError

    @classmethod
    def from_list(cls, source_list):
        # TODO(jasonpr): Implement once we've reconciled Python lists
        # with Lisp lists.
        raise NotImplementedError

    def fill(self, fill_value):
        new_backing_list = [fill_value] * self.length()
        self._elements = new_backing_list

    def __repr__(self):
        return '#(' + ' '.join(str(elt) for elt in self._elements) + ')'

class _Boolean(DataType):
    """A boolean, with a Scheme-like #t/#f representation."""
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return '#t' if self._value else '#f'

_lisp_true = _Boolean(True)
_lisp_false = _Boolean(False)

def lisp_bool(value):
    """Gets the _Boolean representation of True and False."""
    return _lisp_true if value else _lisp_false


class _Null(DataType):
    """The empty list, which is NOT a pair!

    Only one null object shall ever be created.  It is datatypes.null,
    and it is created below.
    """
    def __repr__(self):
        return '()'

null = _Null()

def is_null(data):
    """Returns whether an object is the (singleton) null object."""
    return data is null
