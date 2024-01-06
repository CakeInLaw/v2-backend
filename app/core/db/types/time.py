import datetime as dt
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.type_transformers import transform_time
from core.constants import EMPTY
from core.utils import clean_kwargs
from core.settings import settings
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Time", "TimeInfo", "time"]


class Time(TypeDecorator[dt.time]):

    impl: sa.Time
    repr_attrs = ('timezone',)

    def __init__(
            self,
            timezone: bool = False,
            gte: dt.time = None,
            lte: dt.time = None,
    ):
        super().__init__()

        self.impl = sa.Time(timezone=timezone)
        if gte is not None and lte is not None:
            assert lte > gte
        self.gte = gte
        self.lte = lte

    @property
    def timezone(self) -> bool:
        return self.impl.timezone

    def process_result_value(self, value: str | dt.time | None, dialect) -> dt.time | None:
        return transform_time(value)


class TimeInfo(ColumnInfo):
    fmt: str


def time(
        timezone: bool = False,
        gte: dt.time = None,
        lte: dt.time = None,
        fmt: str = settings.default_time_fmt,
        default: dt.time | None = EMPTY,
        default_factory: Callable[[], dt.time | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        read_only: bool = False,
        hidden: bool = False,
        filter_enable: bool = True,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    info = TimeInfo(read_only=read_only, hidden=hidden, filter_enable=filter_enable, fmt=fmt)
    return mapped_column(
        Time(timezone=timezone, gte=gte, lte=lte),
        info=info,
        server_default=server_default,
        **cleaned_kwargs
    )
