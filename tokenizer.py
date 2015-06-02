import cStringIO

import tokens
import string

class TokenSupply(object):
    def __init__(self, tokenizer):
        self._tokenizer = iter(tokenizer)
        self._load_next()

    def _load_next(self):
        try:
            self._peeked_value = next(self._tokenizer)
            while self._peeked_value is None:
                self._peeked_value = next(self._tokenizer)
        except StopIteration:
            self._peeked_value = None

    def discard_peeked_value(self):
        self._peeked_value = None

    def next(self):
        result = self.peek()
        self._peeked_value = None
        return result

    def peek(self):
        if not self._peeked_value:
            self._load_next()
        return self._peeked_value


class Tokenizer(object):
    def __init__(self, open_file):
        self._chars = character_source(open_file)
        self._current_element = []

    def _finish_current_token(self):
        token_text = ''.join(self._current_element)
        self._current_element = []
        return tokens.Element(token_text) if token_text else None

    def __iter__(self):
        for char in self._chars:
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
    for line in lines:
        for character in line:
            yield character
        yield '\n'
