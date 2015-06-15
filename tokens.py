class Token(object):
    """A basic, building-block element of the langauge."""
    pass

class OpenParen(Token):
    """An open parenthesis, which adds a new level to the parse tree."""
    def __repr__(self):
        return 'OpenParen'

class CloseParen(Token):
    """A close parenthesis, which terminates a level of the parse tree."""
    def __repr__(self):
        return 'CloseParen'

class Element(Token):
    """Any node of the parse tree."""
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Element(%s)' % value
