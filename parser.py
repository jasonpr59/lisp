import tokens

def _parse(token_supply):
    """The top-level expression parser."""
    token = token_supply.peek()
    if not token:
        # That's the end!
        return None

    if isinstance(token, tokens.OpenParen):
        return _parse_list(token_supply)
    elif isinstance(token, tokens.Element):
        return _parse_element(token_supply)
    else:
        raise TypeError('Unexpected token type for %s.' % token)


def _parse_list(token_supply):
    """Parse a list, returning a parse tree.

    A list is an OpenParen, followed by zero or more Elements,
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


def _parse_element(token_supply):
    """Parse a non-list, returning an object."""
    element = token_supply.next()
    assert isinstance(element, tokens.Element)
    return element.value


def parse_trees(token_supply):
    """Yields parse trees from an iterable of tokens."""
    ast = _parse(token_supply)
    while ast is not None:
        yield ast
        ast = _parse(token_supply)
