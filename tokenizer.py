import cStringIO

import tokens
import string

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


class Tokenizer(object):
    """An iterator of tokens in a Lisp file."""
    def __init__(self, open_file):
        self._chars = character_source(open_file)
        # We store a token's constinuent characters until we reach a
        # special character. At that point those characters are
        # assembled into a token.
        self._current_element = []
        self._in_comment = False

    def _finish_current_token(self):
        token_text = ''.join(self._current_element)
        self._current_element = []
        return tokens.Element(token_text) if token_text else None

    def __iter__(self):
        for char in self._chars:
            if char == ';':
                self._in_comment = True
            if self._in_comment:
                if char == '\n':
                    self._in_comment = False
                continue

            if char == "(":
                yield self._finish_current_token()
                yield tokens.OpenParen()
            elif char == ")":
                yield self._finish_current_token()
                yield tokens.CloseParen()
            elif char in string.whitespace:
                yield self._finish_current_token()
            else:
                # TODO(jasonpr): Handle escaping.
                self._current_element.append(char)
        yield self._finish_current_token()



def character_source(lines):
    """Yields characters from an iterable over lines of text, such as a file."""
    for line in lines:
        for character in line:
            yield character
        yield '\n'
