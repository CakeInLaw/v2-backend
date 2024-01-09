import datetime as dt
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.type_transformers import transform_datetime
from core.constants import EMPTY
from core.utils import clean_kwargs, default_if_empty
from core.settings import settings
from ._base import TypeDecorator, ColumnInfo


__all__ = ["DateTime", "DateTimeInfo", "datetime"]


class DateTime(TypeDecorator[dt.datetime]):
    cache_ok = True
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

    def process_result_value(self, value: str | dt.datetime | None, dialect) -> dt.datetime | None:
        return transform_datetime(value, with_timezone=self.timezone)


class DateTimeInfo(ColumnInfo):
    fmt: str


def datetime(
        timezone: bool = False,
        gte: dt.datetime = None,
        lte: dt.datetime = None,
        fmt: str = EMPTY,
        default: dt.datetime | None = EMPTY,
        default_factory: Callable[[], dt.datetime | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        read_only: bool = False,
        hidden: bool = False,
        filter_enable: bool = True,
        server_default: str | sa.TextClause = None,
        auto_now_add: bool = False
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    info = DateTimeInfo(
        read_only=read_only, hidden=hidden, filter_enable=filter_enable,
        fmt=default_if_empty(fmt, settings.default_datetime_fmt)
    )
    if auto_now_add:
        server_default = sa.func.now()
    return mapped_column(
        DateTime(timezone=timezone, gte=gte, lte=lte),
        info=info,
        server_default=server_default,
        **cleaned_kwargs
    )
