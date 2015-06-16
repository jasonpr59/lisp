class Token(object):
    """A basic, building-block element of the langauge."""
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.text)

    def is_parseable(self):
        """Whether this token is meaningful to the parser.

        True by default.  
        """
        return True

class OpenParen(Token):
    """An open parenthesis, which adds a new level to the parse tree."""
    def __repr__(self):
        return 'OpenParen'

class CloseParen(Token):
    """A close parenthesis, which terminates a level of the parse tree."""
    def __repr__(self):
        return 'CloseParen'

class Identifier(Token):
    """Any name or keyword."""

class Integer(Token):
    """An integer, such as 123 or +45 or -67."""

class Whitespace(Token):
    """Whitespace between other tokens."""

    def is_parseable(self):
        return False

class Quote(Token):
    """A single quote."""

class BackQuote(Token):
    """A single backquote (i.e. backtick)."""

class CharLiteral(Token):
    """A character literal, like #\a."""

class BooleanLiteral(Token):
    """A boolean literal, like #f."""

class OpenVector(Token):
    """The begining of a vector description: #(."""

class String(Token):
    """A string, whose text includes surrounding quotes."""

class Comment(Token):
    """A single-line comment, begun with a semicolon."""

    def is_parseable(self):
        return False
