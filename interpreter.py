import string
import types

import pyfuncs
import datatypes

def execute(ast):
    print _eval(ast, base_env)


def _eval(expr, env):
    if isinstance(expr, list):
        return _eval_list(expr, env)
    else:
        return _eval_value(expr, env)


def _eval_value(expr, env):
    # TODO(jasonpr): Move some of this into the lex/parse logic.
    if expr[0] in string.digits:
        return int(expr)
    elif expr[0] == "'":
        return datatypes.Symbol(expr)
    else:
        # Assume it's a variable.
        return env[expr]


def _eval_list(expr, env):
    directive, data = expr[0], expr[1:]
    try:
        evaluator = evaluators[directive]
    except KeyError:
        # It must be a function.  Apply it.
        evaluator = Applier(env[directive], env)
    return evaluator(data)

class Applier(object):
    def __init__(self, function, env):
        self._function = function
        self._env = env

    def __call__(self, lisp_args):
        inputs = [_eval(arg, self._env) for arg in lisp_args]
        if isinstance(self._function, types.FunctionType):
            # It's a builtin Python function.
            return self._function(inputs)

        # Otherwise, it's a LispFunction.
        assert len(inputs) == len(function.arg_names)
        invocation_env = function.env.child()
        for name, value in zip(function.arg_names, inputs):
            invocation_env[name] = value
        return _eval(function.expr, invocation_env)


class Environment(object):
    def __init__(self, parent=None):
        self._vars = {}
        self._parent = parent

    def __getitem__(self, key):
        try:
            return self._vars[key]
        except KeyError:
            if not self._parent:
                raise
            return self._parent[key]

    def __setitem__(self, key, value):
        """Give a value to a name in this environment."""
        self._vars[key] = value

    def child(self):
        return Environment(parent=self)

functions = {
    '+': pyfuncs.add,
    '*': pyfuncs.mul,
    'list': pyfuncs.make_list,
    'cons': pyfuncs.cons,
    'car': pyfuncs.car,
    'cdr': pyfuncs.cdr,
}

base_env = Environment()
for name, value in functions.items():
    base_env[name] = value

evaluators = {}
