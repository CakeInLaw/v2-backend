from decimal import Decimal, InvalidOperation

from core.schemas.models.columns import NumericSchema
from ._base import ColumnValidator
from ..exceptions import (
    NumericGteError, NumericLteError,
    NumericGtError, NumericLtError,
    NumericBigScaleError, NumericBigPrecisionError,
)


__all__ = ["NumericValidator"]


class NumericValidator(ColumnValidator[NumericSchema, Decimal]):
    python_type = Decimal

    def _init_validators(self):
        self._validators.append(self._validate_size)
        if self._schema.gte is not None:
            self._validators.append(self._validate_gte)
        if self._schema.lte is not None:
            self._validators.append(self._validate_lte)
        if self._schema.gt is not None:
            self._validators.append(self._validate_gt)
        if self._schema.lt is not None:
            self._validators.append(self._validate_lt)

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
        return Decimal(f'0.{"0" * (self._schema.scale - 1)}1')

    def _validate_size(self, value: Decimal):
        _, digits, exp = value.as_tuple()
        if self._schema.scale != -exp:
            raise NumericBigScaleError(value=self._schema.scale)
        if self._schema.precision < (len(digits) - self._schema.scale):
            raise NumericBigPrecisionError(value=self._schema.precision)

    def _validate_gte(self, value: Decimal):
        if value < self._schema.gte:
            raise NumericGteError(value=self._schema.gte)

    def _validate_lte(self, value: Decimal):
        if value > self._schema.lte:
            raise NumericLteError(value=self._schema.lte)

    def _validate_gt(self, value: Decimal):
        if value <= self._schema.gte:
            raise NumericGtError(value=self._schema.gt)

    def _validate_lt(self, value: Decimal):
        if value >= self._schema.lte:
            raise NumericLtError(value=self._schema.lt)

