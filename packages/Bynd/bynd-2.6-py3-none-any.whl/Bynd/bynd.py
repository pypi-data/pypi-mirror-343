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
    def ref(cls: type['Bynd'], /) -> '__ByndRef__':
        """Returns a new '__ByndRef__' object instance."""
        return cls._bref

    @classmethod
    def data(cls: type['Bynd'], /) -> Any:
        """Returns the 'Bynd' object instance data."""
        return cls._bynd._data

    @classmethod
    def kind(cls: type['Bynd'], /) -> type:
        """Returns the 'Bynd' object instance data kind."""
        return cls._bynd._kind

    @classmethod
    def inner(cls: type['Bynd'], /) -> set[type]:
        """Returns the 'Bynd' object instance collection elements kind(s)."""
        return cls._bynd._inner

    @classmethod
    def info(cls: type['Bynd'], /) -> tuple[Any, type, set[type]]:
        """Returns a tuple containing the 'Bynd' object instance data, kind, and collection elements kind(s)."""
        return (cls.data(), cls.kind(), cls.inner())
