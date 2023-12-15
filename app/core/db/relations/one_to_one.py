from typing import Any, Callable, Literal, TypedDict

import sqlalchemy as sa

from sqlalchemy.orm import mapped_column, InstrumentedAttribute, relationship

from core.constants import EMPTY
from core.utils import clean_kwargs


__all__ = ["one_to_one", "OneToOneInfo"]


class OneToOneInfo(TypedDict):
    read_only: bool
    hidden: bool


def one_to_one(
        col: str | InstrumentedAttribute | sa.Column,
        *,
        default: Any = EMPTY,
        default_factory: Callable[[], Any] = EMPTY,
        nullable: bool = EMPTY,
        primary_key: bool = False,
        read_only: bool = False,
        hidden: bool = False,
        server_default: str | sa.TextClause = None,
        ondelete: Literal["CASCADE", "RESTRICT", "SET_NULL"] = None,

        back_populates: str = None,
        cascade: str = EMPTY,
        no_relation: bool = False,
):
    unique = True
    if primary_key:
        nullable = False
        unique = False
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
    )
    info = OneToOneInfo(read_only=read_only, hidden=hidden)
    c = mapped_column(
        sa.ForeignKey(col, ondelete=ondelete),
        unique=unique,
        primary_key=primary_key,
        server_default=server_default,
        info=info,
        **cleaned_kwargs
    )
    if no_relation:
        return c
    return c, relationship(
        foreign_keys=[c],
        back_populates=back_populates,
        **clean_kwargs(cascade=cascade),
    )
