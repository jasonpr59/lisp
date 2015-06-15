"""Formats Lisp data for display to a human."""
import datatypes

def lisp_format(value):
    """Format a Lisp value for display to a human."""
    # Do naked formatting, then wrap with parentheses if needed.
    fmt = '(%s)' if isinstance(value, datatypes.Pair) else '%s'
    return fmt % _naked_format(value)

def _naked_format(value):
    """Format a Lisp value, but without grouping with outer parentheses.

    This is corecursive with lisp_format, and correctly displays lists.
    """
    if not isinstance(value, datatypes.Pair):
        return value

    if datatypes.is_null(value.cdr):
        return '%s' % lisp_format(value.car)
    else:
        car = lisp_format(value.car)
        cdr = _naked_format(value.cdr)
        fmt = '%s %s' if isinstance(value.cdr, datatypes.Pair) else '%s . %s'
        return fmt % (car, cdr)
