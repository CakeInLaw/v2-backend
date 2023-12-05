from decimal import Decimal, InvalidOperation
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Numeric", "NumericInfo", "numeric"]


class Numeric(TypeDecorator[float]):
    impl: sa.Numeric
    repr_attrs = ('precision', 'scale')

    def __init__(
            self,
            precision: int,
            scale: int,
            *,
            gte: Decimal = None,
            gt: Decimal = None,
            lte: Decimal = None,
            lt: Decimal = None,
    ):
        super().__init__()
        assert precision > scale >= 1
        self.impl = sa.Numeric(precision=precision, scale=scale)

        has_gte, has_gt, gt_value = gte is not None, gt is not None, None
        has_lte, has_lt, lt_value = lte is not None, lt is not None, None

        if has_gte or has_gt:
            if has_gte and has_gt:
                raise ValueError('Can`t provide both gte and gt')
            gte = self.normalize(gte) if has_gte else gte
            gt = self.normalize(gt) if has_gt else gt
            gt_value = gte if has_gte else gt

        if has_lte or has_lt:
            if has_lte and has_lt:
                raise ValueError('Can`t provide both lte and lt')
            lte = self.normalize(lte) if has_lte else lte
            lt = self.normalize(lt) if has_lt else lt
            lt_value = lte if has_lte else lt

        if gt_value is not None and lt_value is not None:
            assert gt_value > lt_value

        self.gte = gte
        self.gt = gt
        self.lte = lte
        self.lt = lt

    @property
    def precision(self) -> int:
        return self.impl.precision

    @property
    def scale(self) -> int:
        return self.impl.scale

    @property
    def step(self) -> Decimal:
        return Decimal(f'0.{"0" * (self.scale - 1)}1')

    def to_decimal(self, raw: str | int | float):
        try:
            value = Decimal(raw)
        except InvalidOperation:
            raise ValueError(f'Incorrect decimal value, {raw}')
        return self.normalize(value)

    def normalize(self, value: Decimal) -> Decimal:
        return value.quantize(self.step)

    def responds(self, value: Decimal) -> bool:
        _, digits, exp = value.as_tuple()
        return (
            self.scale == -exp  # comparing right path of decimal
            and self.precision >= (len(digits) - self.scale)  # comparing left part of decimal
        )

    def process_bind_param(self, value: Decimal, dialect):
        if value is None:
            return
        return self.normalize(value)


class NumericInfo(ColumnInfo):
    pass


def numeric(
        precision: int,
        scale: int,
        *,
        gte: Decimal = None,
        gt: Decimal = None,
        lte: Decimal = None,
        lt: Decimal = None,
        positive: bool = False,
        non_negative: bool = False,
        negative: bool = False,
        non_positive: bool = False,
        default: Decimal | None = EMPTY,
        default_factory: Callable[[], Decimal | None] = EMPTY,
        nullable: bool = EMPTY,
        unique: bool = EMPTY,
        read_only: bool = False,
        server_default: str | sa.TextClause = None,
):
    cleaned_kwargs = clean_kwargs(
        default=default,
        default_factory=default_factory,
        nullable=nullable,
        unique=unique,
    )
    info = NumericInfo(read_only=read_only)

    gt = Decimal('0') if positive else gt
    gte = Decimal('0') if non_negative else gte
    lt = Decimal('0') if negative else lt
    lte = Decimal('0') if non_positive else lte

    return mapped_column(
        Numeric(precision=precision, scale=scale, gte=gte, gt=gt, lte=lte, lt=lt),
        info=info,
        server_default=server_default,
        **cleaned_kwargs,
    )
