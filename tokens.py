class Token(object):
    pass

class OpenParen(Token):
    def __repr__(self):
        return 'OpenParen'

class CloseParen(Token):
    def __repr__(self):
        return 'CloseParen'

class Element(Token):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Element(%s)' % value
