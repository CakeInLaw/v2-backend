from decimal import Decimal
from typing import Any, Generic, TypeVar, Self, TYPE_CHECKING
from datetime import date, datetime, time


T = TypeVar('T')


class ColumnValidationError(Exception):
    def __init__(self, _code: str, **kwargs):
        self.code = _code
        self.kw = kwargs

    @property
    def params(self) -> dict[str, Any]:
        return self.kw

    def __call__(self, **kwargs):
        kw = {**self.kw, **kwargs} if self.kw else kwargs
        return self.__class__(self.code, **kw)

    def export(self):
        return {'code': self.code, 'params': self.params}


class _VColumnValidationError(ColumnValidationError, Generic[T]):
    if TYPE_CHECKING:
        def __call__(self, value: T, **kwargs) -> Self: ...


NonNullable = ColumnValidationError('non_nullable')

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
