from decimal import Decimal
from typing import Generic, TypeVar, Self
from datetime import date, datetime, time

from ._base import ValidationError


T = TypeVar('T')
__all__ = [
    "ColumnValidationError",
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


DateGteError = _VColumnValidationError[date]('types.date.gte')
DateLteError = _VColumnValidationError[date]('types.date.lte')

DateTimeGteError = _VColumnValidationError[datetime]('types.datetime.gte')
DateTimeLteError = _VColumnValidationError[datetime]('types.datetime.lte')
DateTimeTimezoneAwareError = ColumnValidationError('types.datetime.tz_aware')
DateTimeTimezoneNaiveError = ColumnValidationError('types.datetime.tz_naive')

IntegerGteError = _VColumnValidationError[int]('types.integer.gte')
IntegerLteError = _VColumnValidationError[int]('types.integer.lte')

NumericGteError = _VColumnValidationError[Decimal]('types.numeric.gte')
NumericGtError = _VColumnValidationError[Decimal]('types.numeric.gt')
NumericLteError = _VColumnValidationError[Decimal]('types.numeric.lte')
NumericLtError = _VColumnValidationError[Decimal]('types.numeric.lt')
NumericBigScaleError = _VColumnValidationError[int]('types.numeric.big_scale')
NumericBigPrecisionError = _VColumnValidationError[int]('types.numeric.big_precision')

StringMinLengthError = _VColumnValidationError[int]('types.string.min_length')
StringMaxLengthError = _VColumnValidationError[int]('types.string.max_length')
StringPatternError = ColumnValidationError('types.string.incorrect_pattern')

TimeGteError = _VColumnValidationError[time]('types.time.gte')
TimeLteError = _VColumnValidationError[time]('types.time.lte')
