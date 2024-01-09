from decimal import Decimal
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.type_transformers import transform_string
from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["String", "StringInfo", "string"]


class String(TypeDecorator[str]):
    cache_ok = True
    impl: sa.String
    repr_attrs = ('max_length', )

    def __init__(
            self,
            *,
            min_length: int = None,
            max_length: int = None,
    ):
        super().__init__()

        self.impl = sa.String(length=max_length)
        self.min_length = min_length

    @property
    def max_length(self) -> int | None:
        return self.impl.length

    def process_result_value(self, value: int | float | Decimal | str | None, dialect) -> bool | None:
        return transform_string(value)


class StringInfo(ColumnInfo):
    pattern: str | None


def string(
        *,
        min_length: int = None,
        max_length: int = None,
        default: str | None = EMPTY,
        default_factory: Callable[[], str | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        primary_key: bool = False,
        read_only: bool = False,
        hidden: bool = False,
        filter_enable: bool = True,
        pattern: str = None,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    info = StringInfo(read_only=read_only, hidden=hidden, filter_enable=filter_enable, pattern=pattern)
    return mapped_column(
        String(min_length=min_length, max_length=max_length),
        primary_key=primary_key,
        info=info,
        server_default=server_default,
        **cleaned_kwargs,
    )
