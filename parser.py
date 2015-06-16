import datatypes
import tokens


def _parse_list(token_supply):
    """Parse a list, returning a parse tree.

    A list is an OpenParen, followed by zero or more expressions,
    completed by a CloseParen.
    """
    paren = token_supply.next()
    assert isinstance(paren, tokens.OpenParen)

    result = []
    while not isinstance(token_supply.peek(), tokens.CloseParen):
        result.append(_parse(token_supply))
    # Move past the closing parenthesis.
    token_supply.discard_peeked_value()
    return result


def _parse_identifier(token_supply):
    """Parse a non-list, returning an object."""
    identifier = token_supply.next()
    assert isinstance(identifier, tokens.Identifier)
    return identifier.text


def _parse_integer(token_supply):
    """Parse an integer.

    Returns a fraction, because all rational numbers are represented
    as fractions.
    """
    int_token = token_supply.next()
    assert isinstance(int_token, tokens.Integer)
    return datatypes.Fraction(int(int_token.text))

def _parse_quotation(token_supply):
    """Parse a symbol."""
    quote_token = token_supply.next()
    assert isinstance(quote_token, tokens.Quote)
    quoted_token = token_supply.next()
    if isinstance(quoted_token, tokens.OpenParen):
        # TODO(jasonpr): Implement deep quoting.
        raise NotImplementedError('We can only quote single tokens for now.')
    return datatypes.Symbol(quoted_token.text)

def _parse_boolean(token_supply):
    """Parse a boolean literal."""
    boolean_token = token_supply.next()
    assert isinstance(boolean_token, tokens.BooleanLiteral)
    text = boolean_token.text.lower()
    if text == '#t':
        return datatypes.lisp_bool(True)
    elif text == '#f':
        return datatypes.lisp_bool(False)
    else:
        raise ValueError('Unexpected boolean literal `%s`.' % text)


# Which handler to invoke when a token is encountered in a top-level
# parse context.
_handlers = (
    (tokens.OpenParen, _parse_list),
    (tokens.Identifier, _parse_identifier),
    (tokens.Integer, _parse_integer),
    (tokens.Quote, _parse_quotation),
    (tokens.BooleanLiteral, _parse_boolean),
)

def _parse(token_supply):
    """The top-level expression parser."""
    token = token_supply.peek()
    if not token:
        # That's the end!
        return None

    for token_type, handler in _handlers:
        if isinstance(token, token_type):
            return handler(token_supply)
    else:
        raise TypeError('Unexpected token type for %s.' % token)


def parse_trees(token_supply):
    """Yields parse trees from an iterable of tokens."""
    ast = _parse(token_supply)
    while ast is not None:
        yield ast
        ast = _parse(token_supply)
