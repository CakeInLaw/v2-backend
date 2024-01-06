from enum import IntEnum, StrEnum
from typing import Type, Callable, Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.type_transformers import transform_enum
from core.types import ENUM
from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Enum", "EnumInfo", "enum"]


class Enum(TypeDecorator[ENUM]):
    cache_ok = True

    enum_type: Type[ENUM]

    def __init__(self, enum_type: Type[ENUM]):
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

    def process_bind_param(self, value: int | str | ENUM | None, dialect):
        value = transform_enum(value, self.enum_type)
        if value is None:
            return
        return value.value

    def process_result_value(self, value: int | str | ENUM | None, dialect) -> Optional[ENUM]:
        return transform_enum(value, self.enum_type)


class EnumInfo(ColumnInfo):
    pass


def enum(
        enum_type: Type[ENUM],
        default: Optional[ENUM] = EMPTY,
        default_factory: Callable[[], Optional[ENUM]] = EMPTY,
        nullable: bool = EMPTY,
        read_only: bool = False,
        hidden: bool = False,
        filter_enable: bool = True,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
    )
    info = EnumInfo(read_only=read_only, hidden=hidden, filter_enable=filter_enable)

    return mapped_column(
        Enum(enum_type),
        info=info,
        server_default=server_default,
        **cleaned_kwargs,
    )
