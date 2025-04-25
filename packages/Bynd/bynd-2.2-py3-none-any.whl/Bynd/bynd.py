"""Allows binding data input to a single type."""


from .__bynd__ import __Bynd__
from .__byndref__ import __ByndRef__
from typing import Any


class Bynd(object):
    """Binds data input to a single type and collection elements to one or more types.

    Usage:
        bound_data = Bynd("some string", str)
        print(bound_data.data)

    In the example above, '"some string"' is bound to the type 'str'. Otherwise, 
    a ByndError is raised.
    """
    __slots__ = frozenset({})

    def __new__(cls: type['Bynd'], data: Any, kind: type, /, inner: set[type] = set({})) -> 'Bynd':
        """Returns a new 'Bynd' object instance."""
        cls._bynd = __Bynd__(data, kind, inner=inner)
        cls._bref = __ByndRef__(cls._bynd)
        return super(Bynd, cls).__new__(cls)

    @classmethod
    def bynd_ref(cls: type['Bynd'], /) -> '__ByndRef__':
        """Returns a new '__ByndRef__' object instance."""
        return cls._bref
