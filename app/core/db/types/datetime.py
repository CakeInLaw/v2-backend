import datetime as dt
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["DateTime", "DateTimeInfo", "datetime"]


class DateTime(TypeDecorator[dt.datetime]):

    impl: sa.DateTime | sa.TIMESTAMP
    repr_attrs = ('timezone',)

    def __init__(
            self,
            timezone: bool = False,
            gte: dt.datetime = None,
            lte: dt.datetime = None,
    ):
        super().__init__()

        if timezone:
            self.impl = sa.TIMESTAMP(timezone=True)
        else:
            self.impl = sa.DateTime(timezone=False)
        if gte is not None and lte is not None:
            assert lte > gte
        self.gte = gte
        self.lte = lte

    @property
    def timezone(self) -> bool:
        return self.impl.timezone


class DateTimeInfo(ColumnInfo):
    fmt: str


def datetime(
        timezone: bool = False,
        gte: dt.datetime = None,
        lte: dt.datetime = None,
        fmt: str = '%d.%m.%Y %H:%M:%S',
        default: dt.datetime | None = EMPTY,
        default_factory: Callable[[], dt.datetime | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        read_only: bool = False,
        server_default: str | sa.TextClause = None,
        auto_now_add: bool = False
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    info = DateTimeInfo(read_only=read_only, fmt=fmt)
    if auto_now_add:
        server_default = sa.func.now()
    return mapped_column(
        DateTime(timezone=timezone, gte=gte, lte=lte),
        info=info,
        server_default=server_default,
        **cleaned_kwargs
    )
