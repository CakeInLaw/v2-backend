from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Boolean", "BooleanInfo", "boolean"]


class Boolean(TypeDecorator[bool]):
    impl: sa.Boolean
    repr_attrs = ()

    def __init__(self):
        super().__init__()

        self.impl = sa.Boolean()


class BooleanInfo(ColumnInfo):
    pass


def boolean(
        default: bool | None = EMPTY,
        default_factory: Callable[[], bool | None] = EMPTY,
        nullable: bool = EMPTY,
        read_only: bool = False,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
    )
    info = BooleanInfo(read_only=read_only)

    return mapped_column(
        Boolean(),
        info=info,
        server_default=server_default,
        **cleaned_kwargs,
    )