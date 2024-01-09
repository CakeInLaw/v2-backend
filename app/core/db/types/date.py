import datetime as dt
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.type_transformers import transform_date
from core.constants import EMPTY
from core.utils import clean_kwargs, default_if_empty
from core.settings import settings
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Date", "DateInfo", "date"]


class Date(TypeDecorator[dt.date]):
    cache_ok = True
    impl: sa.Date
    repr_attrs = ()

    def __init__(
            self,
            gte: dt.date = None,
            lte: dt.date = None,
    ):
        super().__init__()

        self.impl = sa.Date()
        if gte is not None and lte is not None:
            assert lte > gte
        self.gte = gte
        self.lte = lte

    def process_result_value(self, value: str | dt.date | None, dialect) -> dt.date | None:
        return transform_date(value)


class DateInfo(ColumnInfo):
    fmt: str


def date(
        gte: dt.date = None,
        lte: dt.date = None,
        fmt: str = EMPTY,
        default: dt.date | None = EMPTY,
        default_factory: Callable[[], dt.date | None] = EMPTY,
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
    info = DateInfo(
        read_only=read_only, hidden=hidden, filter_enable=filter_enable,
        fmt=default_if_empty(fmt, settings.default_date_fmt)
    )
    return mapped_column(
        Date(gte=gte, lte=lte),
        info=info,
        server_default=server_default,
        **cleaned_kwargs
    )
