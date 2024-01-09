from decimal import Decimal
from typing import Callable

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column

from core.type_transformers import transform_numeric
from core.constants import EMPTY
from core.utils import clean_kwargs
from ._base import TypeDecorator, ColumnInfo


__all__ = ["Numeric", "NumericInfo", "numeric"]


class Numeric(TypeDecorator[float]):
    cache_ok = True
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
        self.impl = sa.Numeric(precision=precision, scale=scale, asdecimal=True)

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

    def process_bind_param(self, value: Decimal, dialect):
        return transform_numeric(value, self.precision, self.scale)

    def process_result_value(self, value: int | str | None, dialect) -> bool | None:
        return transform_numeric(value, self.precision, self.scale)


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
    info = NumericInfo(read_only=read_only, hidden=hidden, filter_enable=filter_enable)

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
