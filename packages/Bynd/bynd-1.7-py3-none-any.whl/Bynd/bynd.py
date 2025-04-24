"""A module which allows binding data to one or more kind.

Bynd's intended use, is to be assigned to a variable.

Which, in this case, the variable can still be used

exactly the same way just by accessing the 'data'

class attribute. Since 'Bynd' "binds" the data to 

a single type, the data cannot be modified

causing it to be constant and forces the programmer

to create references which can be modified. Inner

collection types can be specified using the 'inner'

keyword argument and passing it a 'set' of types, to

which the collection elements will be bound.
   
The benefits of using Bynd are:

1. Runtime type checking

2. Constant data
   
3. Ability to access the Bynd info
   with the 'info' class attribute
   just the data itself from the 
   variable in which it is stored
   using the 'data' attribute
"""


import sys
from typing import Any
from collections import defaultdict, deque, UserDict, UserList, OrderedDict


def __dir__() -> list[str]:
    """Returns a list of strings corresponding to each 'Bynd' module object."""
    attrs = ['ByndError', 'Bynd']
    return sorted(attrs)


class ByndError(BaseException):
    """Custom error for the 'Bynd' class."""
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

    def __dir__(self: 'ByndError', /) -> list[str]:
        """Returns a list of strings corresponding to each 'ByndError' method."""
        attrs = ['__new__', '__init__']
        return sorted(attrs)


class Bynd(object):
    """Binds data to one or more kind.

    Usage:
        bound_data = Bynd("some string", {str})
        print(bound_data.data)

    In the example above, '"some string"'

    is bound to the type 'str'. Otherwise, 

    a ByndError is raised.
    """
    __slots__ = frozenset({})

    def __new__(cls: type['Bynd'], data: Any, kind: type, /, inner: set[type] = set({})) -> 'Bynd':
        """Return a new 'Bynd' object instance."""
        if not isinstance(kind, type):
            raise ByndError(f"Bynd(..., {kind.__name__}, ...) parameter must be of type 'type' or 'None'")
        elif (len(inner) > 0) and (not all([ isinstance(T, type) for T in inner ])):
            raise ByndError(f"Bynd(..., ..., inner={inner!r}) items must be of type 'type'")
        else:
            cls.data, cls._kind, cls._inner, cls.info = data, kind, inner, list()
            cls.data = cls.__validate__(cls.data)
            cls.info.append((cls.data, kind, inner))
            return super(Bynd, cls).__new__(cls)

    def __dir__(self: 'Bynd', /) -> list[str]:
        """Returns a list of strings corresponding to each 'Bynd' method."""
        attrs = ['__new__', '__init__', '__dir__', '__info__']
        return sorted(attrs)

    def __hash__(self: 'Bynd', /) -> int:
        """Allow 'Bynd' to be hashable."""
        return hash(self)

    @classmethod
    def __retrieve__(cls: type['Bynd'], data: Any, /) -> str:
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
                raise ByndError(f"Bynd({data}) item({data!r}) parameter must be of type {cls._kind.__name__}")
            else:
                return "regular"

    @classmethod
    def __traverse_mapping__(cls: type['Bynd'], data: Any, /) -> object:
        """Traverses and validates the inner kind for a collection mapping."""
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
    def __traverse_sequence__(cls: type['Bynd'], data: Any, /) -> Any:
        """Traverses and validates the inner kind for a collection sequence."""
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
    def __validate__(cls: type['Bynd'], data: Any, /) -> Any:
        """Allows type specification for collection inner kind such as dict, frozenset, list, set, tuple, and others."""
        datatype = cls.__retrieve__(data)

        match datatype:
            case "mapping":
                return cls.__traverse_mapping__(dict(data))
            case "sequence":
                return cls.__traverse_sequence__(list(data))
            case "regular":
                return cls.data
