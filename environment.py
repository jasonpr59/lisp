class Environment(object):
    """A Lisp environment."""
    def __init__(self, parent=None):
        self._vars = {}
        self._parent = parent

    def __getitem__(self, name):
        """Lookup the object for a name in this environment.

        Recurses up to the root environment, and raises a KeyError
        if the name is not found anywhere.
        """
        try:
            return self._vars[name]
        except KeyError:
            if not self._parent:
                raise
            return self._parent[name]

    def __setitem__(self, name, value):
        """Give a value to a name in this environment."""
        self._vars[name] = value

    def redefine(self, name, new_value):
        """Give a new value to a pre-existing name.

        If the name is not yet set in this environment, recurse upwards.
        Raise a KeyError if the name is not found anywhere.
        """
        if name in self._vars:
            original = self._vars[name]
            self._vars[name] = new_value
            return original
        elif not self._parent:
            raise KeyError
        else:
            return self._parent.redefine(name, new_value)

    def child(self):
        """Create an Environment whose parent is this Environment."""
        return Environment(parent=self)
