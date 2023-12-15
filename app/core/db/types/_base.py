from inspect import getfullargspec
from typing import TypedDict, TypeVar, Any

import sqlalchemy as sa


__all__ = ["TypeDecorator", "ColumnInfo"]


T = TypeVar('T', bound=Any)


class TypeDecorator(sa.TypeDecorator[T]):
    cache_ok = True
    repr_attrs: tuple[str, ...] = None

    def __init__(self):
        pass

    def __repr__(self):
        if self.repr_attrs is None:
            attrs = tuple(getfullargspec(self.__class__.__init__).annotations)
        else:
            attrs = self.repr_attrs
        kw_strings = {k: v for k in attrs if (v := getattr(self, k, None)) is not None}
        return f'{self.__class__.__name__}({", ".join(f"{k}={v}" for k, v in kw_strings.items())})'


class ColumnInfo(TypedDict):
    read_only: bool
    hidden: bool
