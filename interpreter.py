"""The interpreter, including the eval-apply magic.

Implements proper tail recursion using _DelayedCalls.
"""

import string

import datatypes

def execute(ast, env):
    """The simple public interface to the evaluation system.

    Evaluates an expression in a base environment and returns the result.
    """
    return _eval(ast, env)


def _eval(expr, env, force=True):
    """Evaluate an expression in an environment.

    If 'force' is False, then this function may return a _DelayedCall,
    which would need to be resolved later on.  If 'force' is True, a
    _DelayedCall may not be returned unresolved: we must resolve it before
    returning.
    """
    value  = _eval_no_force(expr, env)
    if force:
        while isinstance(value, _DelayedCall):
            value = _eval_begin(value.function.exprs, value.invocation_env)
    return value


def _eval_no_force(expr, env):
    """Evaluate an expression in an environment.

    This function may return a _DelayedCall-- it will not force the
    immediate resolution of a result.
    """
    if isinstance(expr, list):
        return _eval_list(expr, env)
    else:
        return _eval_value(expr, env)


def _eval_value(expr, env):
    """Evaluate a non-list in an environment."""
    if isinstance(expr, str):
        # Strings represent variables.
        return env[expr]
    else:
        # Everything else evaluates to itself.
        return expr

def _eval_list(expr, env):
    """Evaluate a list.

    This may be special syntax, or it maybe be a function call.
    """
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
    """Apply a function.

    When an Applier object is called, with some Lisp arguments and an
    environment, the args are first evaluated in that environment. Then,
    they are passed to the function itself.  If the function is a
    LispFunction, the application involves evaluating the function's body.
    """
    def __init__(self, function):
        self._function = function

    def __call__(self, lisp_args, env):
        """Evaluate the arguments and apply the function."""
        inputs = [_eval(arg, env) for arg in lisp_args]
        if isinstance(self._function, datatypes.LispFunction):
            # It's a LispFunction.
            assert len(inputs) == len(self._function.arg_names)
            invocation_env = self._function.env.child()
            for name, value in zip(self._function.arg_names, inputs):
                invocation_env[name] = value
            # Return a delayed call, and let the calling context determine
            # whether it must be resolved immediately.
            return _DelayedCall(self._function, invocation_env)
        else:
            # It's a builtin Python function.
            return self._function(*inputs)


# Evaluators.
def _eval_if(data, env):
    """Evaluate an 'if' expression."""
    assert len(data) == 3
    cond_expr, true_case_expr, false_case_expr = data
    cond_value = _eval(cond_expr, env)

    result_expr = true_case_expr if _is_truthy(cond_value) else false_case_expr
    return _eval(result_expr, env, force=False)


def _eval_define(data, env):
    """Evaluate a 'define' expression."""
    assert data
    defined = data[0]

    if isinstance(defined, list):
        assert len(data) >= 2
        _eval_define_function(defined, data[1:], env)
    else:
        assert len(data) == 2
        _eval_define_variable(defined, data[1], env)


def _eval_define_variable(name, expr, env):
    """Helper function for defining a variable with a value."""
    env[name] = _eval(expr, env)


def _eval_define_function(definition_spec, implementation, env):
    """Helper function for defining a function."""
    assert definition_spec
    func_name, arg_names = definition_spec[0], definition_spec[1:]
    env[func_name] = datatypes.LispFunction(env, arg_names, implementation)


def _eval_lambda(data, env):
    """Evaluate a 'lambda' expression."""
    assert len(data) >= 2
    arg_names, implementation = data[0], data[1:]
    return datatypes.LispFunction(env, arg_names, implementation)


def _eval_set(data, env):
    """Evaluate a 'set!' expression."""
    assert len(data) == 2
    name, expr = data
    return env.redefine(name, _eval(expr, env))

def _eval_begin(expressions, env):
    """Evaluate a sequence of expressions.

    The resulting value is the last expression's value.
    """
    for expression in expressions[:-1]:
        result = _eval(expression, env)

    if expressions:
        # The last one may be in a tail context, so we do not force
        # it.
        return _eval(expressions[-1], env, force=False)
    else:
        # An empty begin has no effect and returns nothing.
        return None

def _eval_let(data, enclosing_env):
    """Evaluate a 'let' expression."""
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

def _eval_quote(data, env):
    assert len(data) == 1
    quoted_syntax_tree = data[0]
    if isinstance(quoted_syntax_tree, list):
        # TODO(jasonpr): Use a Lisp list.
        return [_eval_quote([subtree], env) for subtree in quoted_syntax_tree]
    else:
        return datatypes.Symbol(quoted_syntax_tree)


evaluators = {
    'if': _eval_if,
    'define': _eval_define,
    'lambda': _eval_lambda,
    'set!': _eval_set,
    'begin': _eval_begin,
    'let': _eval_let,
    'quote': _eval_quote,
}


class _DelayedCall(object):
    """The data needed to carry out a function call.

    Commonly, these calls will be forced as soon as they are created.
    But, when a delayed call is created in a tail context, some cleanup
    is performed before the call is forced.  This allows us to bound the
    height of the stack when performing tail recursion.
    """

    def __init__(self, function, invocation_env):
        self.function = function
        self.invocation_env = invocation_env


def _is_truthy(value):
    """Return False iff value is #f."""
    # Scheme defines nearly everything to be truthy.  Only #f is falsey!
    # TODO(jasonpr): Consider violating the Scheme spec, and doing
    # something more Pythonic.
    return value != datatypes.lisp_bool(False)
