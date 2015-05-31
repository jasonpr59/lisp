import string
import types

import pyfuncs
import datatypes

def execute(ast):
    return _eval(ast, base_env)


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
    if not expr:
        # It's a null value
        return datatypes.null

    directive, data = expr[0], expr[1:]
    if isinstance(directive, str) and directive in evaluators:
        evaluator = evaluators[directive]
    else:
        # It must be a function.  Apply it.
        function = _eval(directive, env)
        evaluator = Applier(function)
    return evaluator(data, env)

class Applier(object):
    def __init__(self, function):
        self._function = function

    def __call__(self, lisp_args, env):
        inputs = [_eval(arg, env) for arg in lisp_args]
        if isinstance(self._function, types.FunctionType):
            # It's a builtin Python function.
            return self._function(inputs)

        # Otherwise, it's a LispFunction.
        assert len(inputs) == len(self._function.arg_names)
        invocation_env = self._function.env.child()
        for name, value in zip(self._function.arg_names, inputs):
            invocation_env[name] = value
        return _eval(self._function.expr, invocation_env)


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


base_env = Environment()
for name, value in pyfuncs.functions.items():
    base_env[name] = value

# Evaluators.
def _eval_if(data, env):
    assert len(data) == 3
    cond_expr, true_case_expr, false_case_expr = data
    cond_value = _eval(cond_expr, env)
    # Just use Python's truthiness rules.
    # TODO(jasonpr): Implement custom truthiness rules.
    result_expr = true_case_expr if cond_value else false_case_expr
    return _eval(result_expr, env)

def _eval_define(data, env):
    assert len(data) == 2
    name, expr = data
    env[name] = _eval(expr, env)

def _eval_lambda(data, env):
    assert len(data) == 2
    arg_names, implementation = data
    return datatypes.LispFunction(env, arg_names, implementation)

evaluators = {
    'if': _eval_if,
    'define': _eval_define,
    'lambda': _eval_lambda,
}
