import string
import types

import datatypes
import environment
import pyfuncs

# Setup the base environment.
base_env = environment.Environment()
for name, value in pyfuncs.functions.items():
    base_env[name] = value


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
    elif expr[0] == '#':
        if expr == '#t':
            return datatypes.lisp_bool(True)
        elif expr == '#f':
            return datatypes.lisp_bool(False)
        else:
            raise ValueError('Unexpected literal `%s`.' % expr)
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


# Evaluators.
def _eval_if(data, env):
    assert len(data) == 3
    cond_expr, true_case_expr, false_case_expr = data
    cond_value = _eval(cond_expr, env)

    result_expr = true_case_expr if _is_truthy(cond_value) else false_case_expr
    return _eval(result_expr, env)


def _eval_define(data, env):
    assert len(data) == 2
    name, expr = data
    env[name] = _eval(expr, env)


def _eval_lambda(data, env):
    assert len(data) == 2
    arg_names, implementation = data
    return datatypes.LispFunction(env, arg_names, implementation)


def _eval_set(data, env):
    assert len(data) == 2
    name, expr = data
    return env.redefine(name, _eval(expr, env))

def _eval_begin(expressions, env):
    result = None
    for expression in expressions:
        result = _eval(expression, env)
    return result

def _eval_let(data, enclosing_env):
    assert data
    bindings, exprs = data[0], data[1:]

    # Setup the new environment.
    new_env = enclosing_env.child()
    for binding in bindings:
        assert len(binding) == 2
        name, expr = binding
        # Evaluate the expression in the enclosing environment,  and
        # bind it into the new one.
        new_env[name] = _eval(expr, enclosing_env)

    # Evaluate the body expressions in the new environment,
    # as though they were enclosed in a `begin` statement.
    return _eval_begin(exprs, new_env)

evaluators = {
    'if': _eval_if,
    'define': _eval_define,
    'lambda': _eval_lambda,
    'set!': _eval_set,
    'begin': _eval_begin,
    'let': _eval_let,
}


def _is_truthy(value):
    # Scheme defines nearly everything to be truthy.  Only #f is falsey!
    # TODO(jasonpr): Consider violating the Scheme spec, and doing
    # something more Pythonic.
    return value != datatypes.lisp_bool(False)
