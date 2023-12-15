from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs, default_if_empty
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Guid", "GuidInfo", "guid"]


class Guid(TypeDecorator[UUID]):
    impl = sa.UUID(as_uuid=True)
    repr_attrs = ()
    cache_ok = True


class GuidInfo(ColumnInfo):
    pass


def guid(
        *,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        primary_key: bool = False,
        generated: bool = EMPTY,
        read_only: bool = EMPTY,
        hidden: bool = False,
):
    if primary_key:
        assert unique is EMPTY
        assert nullable is EMPTY
        generated = default_if_empty(generated, True)
        read_only = default_if_empty(read_only, True)
    cleaned_kwargs = clean_kwargs(
        primary_key=primary_key,
        nullable=nullable,
        unique=unique,
        server_default=sa.text('gen_random_uuid()') if generated is not False else EMPTY,
    )
    info = GuidInfo(read_only=read_only, hidden=hidden)
    return mapped_column(
        Guid(),
        info=info,
        **cleaned_kwargs,
    )
