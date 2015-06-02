class Environment(object):
    def __init__(self, parent=None):
        self._vars = {}
        self._parent = parent

    def __getitem__(self, key):
        try:
            return self._vars[key]
        except KeyError:
            if not self._parent:
                raise
            return self._parent[key]

    def __setitem__(self, key, value):
        """Give a value to a name in this environment."""
        self._vars[key] = value

    def redefine(self, key, new_value):
        if key in self._vars:
            original = self._vars[key]
            self._vars[key] = new_value
            return original
        elif not self._parent:
            raise KeyError
        else:
            return self._parent.redefine(key, new_value)

    def child(self):
        return Environment(parent=self)
