from decimal import Decimal
from typing import Generic, TypeVar, Self
from datetime import date, datetime, time

from ._base import ValidationError


T = TypeVar('T')
__all__ = [
    "ColumnValidationError",
    "NonNullable",
    "NotUnique",
    "DateGteError",
    "DateLteError",
    "DateTimeGteError",
    "DateTimeLteError",
    "DateTimeTimezoneAwareError",
    "DateTimeTimezoneNaiveError",
    "IntegerGteError",
    "IntegerLteError",
    "NumericGteError",
    "NumericGtError",
    "NumericLteError",
    "NumericLtError",
    "NumericBigScaleError",
    "NumericBigPrecisionError",
    "StringMinLengthError",
    "StringMaxLengthError",
    "StringPatternError",
    "TimeGteError",
    "TimeLteError",
]


class ColumnValidationError(ValidationError):
    pass


class _VColumnValidationError(ColumnValidationError, Generic[T]):
    def __call__(self, value: T, **kwargs) -> Self:
        return super().__call__(value=value, **kwargs)


NonNullable = ColumnValidationError('non_nullable')
NotUnique = ColumnValidationError('non_unique')

DateGteError = _VColumnValidationError[date]('columns.date.gte')
DateLteError = _VColumnValidationError[date]('columns.date.lte')

DateTimeGteError = _VColumnValidationError[datetime]('columns.datetime.gte')
DateTimeLteError = _VColumnValidationError[datetime]('columns.datetime.lte')
DateTimeTimezoneAwareError = ColumnValidationError('columns.datetime.tz_aware')
DateTimeTimezoneNaiveError = ColumnValidationError('columns.datetime.tz_naive')

IntegerGteError = _VColumnValidationError[int]('columns.integer.gte')
IntegerLteError = _VColumnValidationError[int]('columns.integer.lte')

NumericGteError = _VColumnValidationError[Decimal]('columns.numeric.gte')
NumericGtError = _VColumnValidationError[Decimal]('columns.numeric.gt')
NumericLteError = _VColumnValidationError[Decimal]('columns.numeric.lte')
NumericLtError = _VColumnValidationError[Decimal]('columns.numeric.lt')
NumericBigScaleError = _VColumnValidationError[int]('columns.numeric.big_scale')
NumericBigPrecisionError = _VColumnValidationError[int]('columns.numeric.big_precision')

StringMinLengthError = _VColumnValidationError[int]('columns.string.min_length')
StringMaxLengthError = _VColumnValidationError[int]('columns.string.max_length')
StringPatternError = ColumnValidationError('columns.string.incorrect_pattern')

TimeGteError = _VColumnValidationError[time]('columns.time.gte')
TimeLteError = _VColumnValidationError[time]('columns.time.lte')
