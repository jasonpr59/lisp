import cStringIO

import tokens
import string

class TokenSupply(object):
    def __init__(self, token_list):
        self._token_list = token_list
        self._index = 0

    def advance(self):
        self._index += 1

    def next(self):
        result = self.peek()
        self._index += 1
        return result

    def peek(self):
        if self._index >= len(self._token_list):
            return None
        return self._token_list[self._index]


class Tokenizer(object):
    def __init__(self, open_file):
        self._chars = character_source(open_file)
        self._current_element = []
        self._token_list = []

    def _finish_current_token(self):
        token = ''.join(self._current_element)
        if token:
            self._token_list.append(tokens.Element(token))
        self._current_element = []

    def get_tokens(self):
        for char in self._chars:
            if char == "(":
                self._finish_current_token()
                self._token_list.append(tokens.OpenParen())
            elif char == ")":
                self._finish_current_token()
                self._token_list.append(tokens.CloseParen())
            elif char in string.whitespace:
                self._finish_current_token()
            else:
                # TODO(jasonpr): Handle escaping.
                self._current_element.append(char)
        self._finish_current_token()
        return TokenSupply(self._token_list)


def character_source(lines):
    for line in lines:
        for character in line:
            yield character
        yield '\n'
