from typing import Callable, Literal

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Integer", "SmallInteger", "BigInteger", "IntegerInfo", "integer"]


class Integer(TypeDecorator[int]):
    impl: sa.Integer
    repr_attrs = ()
    _min_min_value = -2147483648
    _max_max_value = 2147483647

    def __init__(
            self,
            *,
            gte: int = None,
            lte: int = None,
    ):
        super().__init__()

        if gte is not None:
            assert self._min_min_value < gte < self._max_max_value
        if lte is not None:
            assert self._min_min_value < lte < self._max_max_value
        if gte is not None and lte is not None:
            assert lte - gte >= 1  # >= 0 and <= 1 for less 2 choices

        self._gte = gte
        self._lte = lte
        self.impl = sa.Integer()

    @property
    def gte(self) -> int:
        return self._min_min_value if self._gte is None else self._gte

    @property
    def lte(self) -> int:
        return self._max_max_value if self._lte is None else self._lte


class SmallInteger(Integer):
    impl = sa.SmallInteger()
    _min_min_value = -32768
    _max_max_value = 32767


class BigInteger(Integer):
    impl = sa.BigInteger()
    _min_min_value = -9223372036854775808
    _max_max_value = 9223372036854775807


class IntegerInfo(ColumnInfo):
    pass


def integer(
        *,
        gte: int = None,
        lte: int = None,
        positive: bool = False,
        non_negative: bool = False,
        negative: bool = False,
        non_positive: bool = False,
        t: Literal["normal", "small", "big"] = 'normal',
        default: int | None = EMPTY,
        default_factory: Callable[[], int | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        autoincrement: bool = "auto",
        primary_key: bool = False,
        read_only: bool = EMPTY,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    if primary_key and autoincrement in (True, 'auto'):
        read_only = True if read_only is EMPTY else read_only
    read_only = False if read_only is EMPTY else read_only
    info = IntegerInfo(read_only=read_only)

    gte = 0 if non_negative else 1 if positive else gte
    lte = 0 if non_positive else -1 if negative else lte

    return mapped_column(
        _types[t](gte=gte, lte=lte),
        primary_key=primary_key,
        info=info,
        server_default=server_default,
        **cleaned_kwargs,
    )


_types = {
    'normal': Integer,
    'small': SmallInteger,
    'big': BigInteger,
}
