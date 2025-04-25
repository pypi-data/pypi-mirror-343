"""Bynds core implementation."""

import sys
from typing import Any
from collections import defaultdict, deque, UserDict, UserList, OrderedDict


class ByndError(BaseException):
    """Custom error for the '__Bynd__' class."""
    __slots__ = frozenset({})

    def __new__(cls: type['ByndError'], message: str, /) -> 'ByndError':
        """Return a new 'ByndError' object."""
        assert isinstance(message, str), f"'{message}' must be of type 'str'"
        return super(ByndError, cls).__new__(cls)

    def __init__(self: 'ByndError', message: str | None) -> None:
        """Initialize a 'ByndError' object instance."""
        super().__init__(message)
        self.__suppress_context__ = True
        sys.tracebacklimit = 0


class __Bynd__(object):
    """The core of Bynd's functionality."""
    __slots__ = frozenset({})

    def __new__(cls: type['__Bynd__'], data: Any, kind: type, /, inner: set[type] = set({})) -> '__Bynd__':
        """Return a new '__Bynd__' object instance."""
        if not isinstance(kind, type):
            raise ByndError(f"Bynd(..., {kind.__name__}, ...) parameter must be of type 'type' or 'None'")
        elif (len(inner) > 0) and (not all([ isinstance(T, type) for T in inner ])):
            raise ByndError(f"Bynd(..., ..., inner={inner!r}) items must be of type 'type'")
        else:
            cls._data, cls._kind, cls._inner = data, kind, inner
            cls._data = cls.__validate__(cls._data)
            return super(__Bynd__, cls).__new__(cls)

    def __hash__(self: '__Bynd__', /) -> int:
        """Allow 'Bynd' to be hashable."""
        return hash(self)

    @classmethod
    def __retrieve__(cls: type['__Bynd__'], data: Any, /) -> str:
        """Get the current type of the data to be bound."""
        formatted_kinds = '{' + ', '.join([_type.__name__ for _type in cls._inner]) + '}'

        if isinstance(cls._kind, (defaultdict, dict, OrderedDict, UserDict)):
            if not all([ isinstance(T, type) for T in cls._inner ]):
                raise ByndError(f"Bynd(..., ..., inner={formatted_kinds}) parameters must be of type 'type'")
            else:
                return "mapping"
        elif isinstance(cls._kind, (deque, list, frozenset, set, tuple, UserList)):
            if not all([ isinstance(T, type) for T in cls._inner ]):
                raise ByndError(f"Bynd(..., ..., inner={formatted_kinds}) parameters must be of type 'type'")
            else:
                return "sequence"
        else:
            if type(data) is not cls._kind:
                raise ByndError(f"Bynd({data!r}) parameter must be of type {cls._kind.__name__}")
            else:
                return "regular"

    @classmethod
    def __traverse_mapping__(cls: type['__Bynd__'], data: Any, /) -> object:
        """Traverses a collection mapping and check its element type against the inner type set."""
        formatted_kinds = '{' + ', '.join([_type.__name__ for _type in cls._inner]) + '}'
        inner_data_temp = [data]

        while len(inner_data_temp) != 0:
            inner_data = inner_data_temp.pop()

            for inner_data_key, inner_data_data in inner_data.items():
                datatype = cls.__retrieve__(inner_data_key)

                if type(inner_data_data) not in cls._inner:
                    raise ByndError(f"Bynd({data}) item({inner_data_data}): must be of type(s) {formatted_kinds}")
                elif  datatype == "sequence":
                    cls.__traverse_sequence__(list(inner_data_key))
                elif datatype == "mapping":
                    inner_data_temp.insert(0, inner_data_data)
                else:
                    continue
        else:
            return data

    @classmethod
    def __traverse_sequence__(cls: type['__Bynd__'], data: Any, /) -> Any:
        """Traverses a collection sequence and check its element type against the inner type set."""
        formatted_kinds = '{' + ', '.join([_type.__name__ for _type in cls._inner]) + '}'
        inner_data_temp = [data]

        while len(inner_data_temp) != 0:
            inner_data = inner_data_temp.pop()

            for inner_data_item in inner_data:
                datatype = cls.__retrieve__(inner_data_item)
                if type(inner_data_item) not in cls._inner:
                    raise ByndError(f"Bynd({data}) item({inner_data_item}): must be of kind(s) {formatted_kinds}")
                elif  datatype == "sequence":
                    inner_data_temp.insert(0, list(inner_data_item))
                elif datatype == "mapping":
                    cls.__traverse_mapping__(dict(inner_data_item))
                else:
                    continue
        else:
            return data

    @classmethod
    def __validate__(cls: type['__Bynd__'], data: Any, /) -> Any:
        """Validates the specified data by utilizing the other 'Bynd' methods."""
        datatype = cls.__retrieve__(data)

        match datatype:
            case "mapping":
                return cls.__traverse_mapping__(dict(data))
            case "sequence":
                return cls.__traverse_sequence__(list(data))
            case "regular":
                return data
