"""Allows for the creation of a modifiable Bynd reference.

This only allows the data to be modified but not the type

the data is bound to while also keeping the original Bynd

object data in tact.
"""


import sys
from .__bynd__ import __Bynd__
from typing import Any


class ByndRefError(BaseException):
    """A custom error for the 'ByndRef' class."""
    __slots__ = frozenset({})

    def __new__(cls: type['ByndRefError'], message: str | None = None, /) -> 'ByndRefError':
        """Returns a new 'ByndRefError' object instance."""
        assert isinstance(message, (str, type(None))), f"{message} must be of type 'str' or 'None'"
        return super(ByndRefError, cls).__new__(cls)

    def __init__(self: 'ByndRefError', message: str | None = None, /) -> None:
        """Initializes a new 'ByndRefError' object instance."""
        super().__init__(message)
        self.__supress_context__ = True
        sys.tracebacklimit = 0


class __ByndRef__(object):
    """Creates a modifiable 'Bynd' instance object."""
    __slots__ = frozenset({})
    _bynd_refs = dict({})
    
    def __new__(cls: type['__ByndRef__'], bynd_instance: __Bynd__, /) -> '__ByndRef__':
        """Returns a new '__ByndRef__' object instance."""
        if not isinstance(bynd_instance, __Bynd__):
            raise ByndRefError(f"ByndRef({bynd_instance}) parameter must be of type 'Bynd'")
        else:
            cls._bynd_instance_id = id(bynd_instance)
            cls._bynd_instance = bynd_instance

            if cls._bynd_instance_id not in cls._bynd_refs.keys():
                cls._bynd_refs.update({cls._bynd_instance_id: cls._bynd_instance})
                return super(__ByndRef__, cls).__new__(cls)
            else:
                return super(__ByndRef__, cls).__new__(cls)

    def __hash__(self: '__ByndRef__', /) -> int:
        """Allow '__ByndRef__' to be hashable."""
        return hash(self)

    @classmethod
    def modify(cls: type['__ByndRef__'], data: Any, /) -> None:
        """Allow modification of the '__ByndRef__' object instance."""
        is_valid = cls._bynd_instance.__validate__(data)
        cls._bynd_refs.update({cls._bynd_instance_id: is_valid})
        return None

    @classmethod
    def data(cls: type['__ByndRef__'], /) -> Any:
        """Returns the '__ByndRef__' object instance data."""
        return cls._bynd_refs[cls._bynd_instance_id]._data

    @classmethod
    def kind(cls: type['__ByndRef__'], /) -> type:
        """Returns the '__ByndRef__' object instance data kind."""
        return cls._bynd_refs[cls._bynd_instance_id]._kind

    @classmethod
    def inner(cls: type['__ByndRef__'], /) -> set[type]:
        """Returns the '__ByndRef__' object instance collection elements kind(s)."""
        return cls._bynd_refs[cls._bynd_instance_id]._inner

    @classmethod
    def info(cls: type['__ByndRef__'], /) -> tuple[Any, type, set[type]]:
        """Returns a tuple containing the '__ByndRef__' object instance data, kind, and collection elements kind(s)."""
        return (cls.data(), cls.kind(), cls.inner())
