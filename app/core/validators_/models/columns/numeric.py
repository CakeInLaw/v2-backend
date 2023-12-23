from decimal import Decimal, InvalidOperation

from core.schemas.models.columns import NumericSchema
from ._base import ColumnValidator
from ...exceptions import (
    NumericGteError, NumericLteError,
    NumericGtError, NumericLtError,
    NumericBigScaleError, NumericBigPrecisionError,
)


__all__ = ["NumericValidator"]


class NumericValidator(ColumnValidator[NumericSchema, Decimal]):
    python_type = Decimal

    def _init_validators(self):
        self.add_validator(self._validate_size)
        if self.schema.gte is not None:
            self.add_validator(self._validate_gte)
        if self.schema.lte is not None:
            self.add_validator(self._validate_lte)
        if self.schema.gt is not None:
            self.add_validator(self._validate_gt)
        if self.schema.lt is not None:
            self.add_validator(self._validate_lt)

    def _transform(self, value: str | int | float | Decimal) -> Decimal:
        if isinstance(value, (str, int, float)):
            try:
                value = Decimal(value)
            except InvalidOperation:
                raise ValueError(f'Incorrect decimal value, {value}')
        if isinstance(value, Decimal):
            return self.normalize(value)

    def normalize(self, value: Decimal):
        return value.quantize(self.step)

    @property
    def step(self) -> Decimal:
        return Decimal(f'0.{"0" * (self.schema.scale - 1)}1')

    def _validate_size(self, value: Decimal):
        _, digits, exp = value.as_tuple()
        if self.schema.scale != -exp:
            raise NumericBigScaleError(value=self.schema.scale)
        if self.schema.precision < (len(digits) - self.schema.scale):
            raise NumericBigPrecisionError(value=self.schema.precision)

    def _validate_gte(self, value: Decimal):
        if value < self.schema.gte:
            raise NumericGteError(value=self.schema.gte)

    def _validate_lte(self, value: Decimal):
        if value > self.schema.lte:
            raise NumericLteError(value=self.schema.lte)

    def _validate_gt(self, value: Decimal):
        if value <= self.schema.gte:
            raise NumericGtError(value=self.schema.gt)

    def _validate_lt(self, value: Decimal):
        if value >= self.schema.lte:
            raise NumericLtError(value=self.schema.lt)
