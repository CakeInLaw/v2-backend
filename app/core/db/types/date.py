import datetime as dt
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs
from core.settings import settings
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Date", "DateInfo", "date"]


class Date(TypeDecorator[dt.date]):

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


class DateInfo(ColumnInfo):
    fmt: str


def date(
        gte: dt.date = None,
        lte: dt.date = None,
        fmt: str = settings.default_date_fmt,
        default: dt.date | None = EMPTY,
        default_factory: Callable[[], dt.date | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        read_only: bool = False,
        hidden: bool = False,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    info = DateInfo(read_only=read_only, hidden=hidden, fmt=fmt)
    return mapped_column(
        Date(gte=gte, lte=lte),
        info=info,
        server_default=server_default,
        **cleaned_kwargs
    )
