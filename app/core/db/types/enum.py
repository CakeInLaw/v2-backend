from enum import IntEnum, StrEnum
from typing import Type, TypeVar, Callable, Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Enum", "EnumInfo", "enum"]

ENUM_TYPE = TypeVar('ENUM_TYPE', IntEnum, StrEnum)


class Enum(TypeDecorator[ENUM_TYPE]):
    cache_ok = True

    enum_type: Type[ENUM_TYPE]

    def __init__(self, enum_type: Type[ENUM_TYPE]):
        super().__init__()

        self.enum_type = enum_type
        if issubclass(self.enum_type, IntEnum):
            self.impl = sa.SmallInteger()
            self.int_type, self.str_type = True, False
        elif issubclass(self.enum_type, StrEnum):
            self.impl = sa.String(length=max(map(len, self.enum_values)))
            self.int_type, self.str_type = False, True
        else:
            raise ValueError('only IntEnum or StrEnum')

    @property
    def enum_values(self):
        return [v.value for v in self.enum_type.__members__.values()]

    def __repr__(self):
        return f'Enum(enums.{self.enum_type.__name__})'

    def process_bind_param(self, value: int | str | ENUM_TYPE | None, dialect):
        if value is None:
            return
        if isinstance(value, self.enum_type):
            return value.value
        if self.int_type and isinstance(value, int) or self.str_type and isinstance(value, str):
            return self.enum_type(value).value
        raise ValueError(f'"{value}" can`t process to "{repr(self)}"')

    def process_result_value(self, value: int | str | None, dialect) -> Optional[ENUM_TYPE]:
        if value is None:
            return None
        return self.enum_type(value)


class EnumInfo(ColumnInfo):
    pass


def enum(
        enum_type: Type[ENUM_TYPE],
        default: Optional[ENUM_TYPE] = EMPTY,
        default_factory: Callable[[], Optional[ENUM_TYPE]] = EMPTY,
        nullable: bool = EMPTY,
        read_only: bool = False,
        hidden: bool = False,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
    )
    info = EnumInfo(read_only=read_only, hidden=hidden)

    return mapped_column(
        Enum(enum_type),
        info=info,
        server_default=server_default,
        **cleaned_kwargs,
    )
