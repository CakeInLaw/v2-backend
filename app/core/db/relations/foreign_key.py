from typing import Any, Callable, Literal, TypedDict

import sqlalchemy as sa

from sqlalchemy.orm import mapped_column, InstrumentedAttribute

from core.constants import EMPTY
from core.utils import clean_kwargs


__all__ = ["foreign_key", "ForeignKeyInfo"]


class ForeignKeyInfo(TypedDict):
    read_only: bool


def foreign_key(
        col: str | InstrumentedAttribute | sa.Column,
        *,
        default: Any = EMPTY,
        default_factory: Callable[[], Any] = EMPTY,
        nullable: bool = EMPTY,
        primary_key: bool = False,
        read_only: bool = False,
        server_default: str | sa.TextClause = None,
        ondelete: Literal["CASCADE", "RESTRICT", "SET_NULL"] = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
    )
    info = ForeignKeyInfo(read_only=read_only)
    return mapped_column(
        sa.ForeignKey(col, ondelete=ondelete),
        primary_key=primary_key,
        server_default=server_default,
        info=info,
        **cleaned_kwargs
    )
