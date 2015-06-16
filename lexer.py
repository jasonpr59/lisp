import re

import tokens

_IDENTIFIER_CHARS = '-+_?!*/:<>=a-zA-Z'
_IDENTIFIER_REGEX = '[%s][%s0-9]*' % (_IDENTIFIER_CHARS, _IDENTIFIER_CHARS)

matchers = (
    (re.compile(r'\('), tokens.OpenParen),
    (re.compile(r'\)'), tokens.CloseParen),
    (re.compile(_IDENTIFIER_REGEX), tokens.Identifier),
    (re.compile(r'(\+|-)?[0-9]+'), tokens.Integer),
    (re.compile(r'\s+'), tokens.Whitespace),
    (re.compile(r"'"), tokens.Quote),
    (re.compile(r'`'), tokens.BackQuote),
    (re.compile(r'#\[a-zA-Z]'), tokens.CharLiteral),
    (re.compile(r'#[tfTF]'), tokens.BooleanLiteral),
    (re.compile(r'#\('), tokens.OpenVector),
    (re.compile(r'"([^"\\]|\\")*"'), tokens.String),
    (re.compile(r';.*$'), tokens.Comment),
)

def first_token(lisp_line):
    """Return the first token from a line of Lisp."""
    for matcher, token_type in matchers:
        match = matcher.match(lisp_line)
        if match:
            return token_type(match.group())
    # If we get here, there's no valid token.
    raise ValueError('No valid token found: "%s".' % lisp_line.strip())

def line_tokens(lisp_line):
    """Yield all tokens from a line of Lisp."""
    while lisp_line:
        token = first_token(lisp_line)
        if token.is_parseable():
            yield token
        lisp_line = lisp_line[len(token.text):]

def lisp_tokens(lisp_lines):
    for line in lisp_lines:
        for token in line_tokens(line):
            yield token

class TokenSupply(object):
    """A peeking iterator of tokens.

    The peeking aspect allows a parser to do one-token lookahead.
    """
    def __init__(self, tokenizer):
        self._tokenizer = iter(tokenizer)
        self._peeked_value = None

    def _load_next(self):
        """Get the next token from the underlying iterator.

        We cache this as the peeked value, and will return it next time
        the `next()` method is called.
        """
        try:
            self._peeked_value = next(self._tokenizer)
            while self._peeked_value is None:
                self._peeked_value = next(self._tokenizer)
        except StopIteration:
            self._peeked_value = None

    def discard_peeked_value(self):
        """Get rid of the current peeked value.

        The next call to peek() or next() will hit the underlying
        iterator.
        """
        self._peeked_value = None

    def next(self):
        """Return and discard the peeked value.

        If the iterator has dried up, return None.
        """
        result = self.peek()
        self._peeked_value = None
        return result

    def peek(self):
        """Return the next token, without advancing.

        Multiple calls to peek() return the same value, assuming no
        other methods are called in the meantime.
        """
        if not self._peeked_value:
            self._load_next()
        return self._peeked_value
