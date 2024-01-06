import re
from typing import Generic, Callable, Iterator, TypeVar, Any, Type, Optional
from datetime import date, datetime, time
from decimal import Decimal

from core import type_transformers, types
from core.schema import (
    C as CONSTRAINT,
    BooleanConstraint, DateConstraint, DateTimeConstraint,
    EnumConstraint, GuidConstraint, IntegerConstraint,
    NumericConstraint, StringConstraint, TimeConstraint, Types
)
from .. import exceptions as err


__all__ = [
    "ConstraintValidator", "CONSTR_VAL", "get_constraints_validator",
    "BooleanConstraintValidator", "DateConstraintValidator", "DateTimeConstraintValidator",
    "EnumConstraintValidator", "GuidConstraintValidator", "IntegerConstraintValidator",
    "NumericConstraintValidator", "StringConstraintValidator", "TimeConstraintValidator",
]


T = TypeVar('T', bound=Any)


class ConstraintValidator(Generic[CONSTRAINT, T]):
    _transform: Callable[[Any], T | None]

    def __init__(self, constr: CONSTRAINT):
        self.constr = constr

    def get_validators(self) -> Iterator[Callable]:
        return iter([])

    def transform(self, value: Any) -> T | None:
        return self._transform(value)


CONSTR_VAL = TypeVar('CONSTR_VAL', bound=ConstraintValidator)


class BooleanConstraintValidator(ConstraintValidator[BooleanConstraint, bool]):
    _transform = type_transformers.transform_bool


class DateConstraintValidator(ConstraintValidator[DateConstraint, date]):
    _transform = type_transformers.transform_date

    def get_validators(self) -> Iterator[Callable]:
        if self.constr.gte is not None:
            yield self._validate_gte
        if self.constr.lte is not None:
            yield self._validate_lte

    def _validate_gte(self, value: date):
        if value < self.constr.gte:
            raise err.DateGteError(value=self.constr.gte)

    def _validate_lte(self, value: date):
        if value > self.constr.lte:
            raise err.DateLteError(value=self.constr.lte)


class DateTimeConstraintValidator(ConstraintValidator[DateTimeConstraint, datetime]):

    def get_validators(self) -> Iterator[Callable]:
        if self.constr.gte is not None:
            yield self._validate_gte
        if self.constr.lte is not None:
            yield self._validate_lte
        if self.constr.with_timezone:
            yield self._validate_aware
        else:
            yield self._validate_naive

    def _validate_gte(self, value: datetime):
        if value < self.constr.gte:
            raise err.DateTimeGteError(value=self.constr.gte)

    def _validate_lte(self, value: datetime):
        if value > self.constr.lte:
            raise err.DateTimeLteError(value=self.constr.lte)

    @staticmethod
    def _validate_naive(value: datetime):
        if value.tzinfo is not None:
            raise err.DateTimeTimezoneNaiveError

    @staticmethod
    def _validate_aware(value: datetime):
        if value.tzinfo is None:
            raise err.DateTimeTimezoneAwareError

    def transform(self, value: str | datetime | None) -> T | None:
        return type_transformers.transform_datetime(value, with_timezone=self.constr.with_timezone)


class EnumConstraintValidator(ConstraintValidator[EnumConstraint, types.ENUM]):

    def transform(self, value: str | int | types.ENUM) -> Optional[types.ENUM]:
        return type_transformers.transform_enum(value, python_enum=self.constr.python_type)


class GuidConstraintValidator(ConstraintValidator[GuidConstraint]):
    _transform = type_transformers.transform_guid


class IntegerConstraintValidator(ConstraintValidator[IntegerConstraint]):
    _transform = type_transformers.transform_integer

    def get_validators(self) -> Iterator[Callable]:
        if self.constr.gte is not None:
            yield self._validate_gte
        if self.constr.lte is not None:
            yield self._validate_lte

    def _validate_gte(self, value: int):
        if value < self.constr.gte:
            raise err.IntegerGteError(value=self.constr.gte)

    def _validate_lte(self, value: int):
        if value > self.constr.lte:
            raise err.IntegerLteError(value=self.constr.lte)


class StringConstraintValidator(ConstraintValidator[StringConstraint]):
    _transform = type_transformers.transform_string

    def __init__(self, constr: StringConstraint):
        super().__init__(constr=constr)
        self.pattern = re.compile(self.constr.pattern) if self.constr.pattern else None

    def get_validators(self) -> Iterator[Callable]:
        if self.constr.min_length is not None:
            yield self._validate_min_length
        if self.constr.max_length is not None:
            yield self._validate_max_length
        if self.constr.pattern is not None:
            yield self._validate_pattern

    def _validate_min_length(self, value: str):
        if len(value) < self.constr.min_length:
            raise err.StringMinLengthError(self.constr.min_length)

    def _validate_max_length(self, value: str):
        if len(value) > self.constr.max_length:
            raise err.StringMaxLengthError(self.constr.max_length)

    def _validate_pattern(self, value: str):
        if not self.pattern.match(value):
            raise err.StringPatternError


class NumericConstraintValidator(ConstraintValidator[NumericConstraint]):

    def get_validators(self) -> Iterator[Callable]:
        yield self._validate_size
        if self.constr.gte is not None:
            yield self._validate_gte
        if self.constr.lte is not None:
            yield self._validate_lte
        if self.constr.gt is not None:
            yield self._validate_gt
        if self.constr.lt is not None:
            yield self._validate_lt

    def _validate_size(self, value: Decimal):
        _, digits, exp = value.as_tuple()
        if self.constr.scale != -exp:
            raise err.NumericBigScaleError(value=self.constr.scale)
        if self.constr.precision < (len(digits) - self.constr.scale):
            raise err.NumericBigPrecisionError(value=self.constr.precision)

    def _validate_gte(self, value: Decimal):
        if value < self.constr.gte:
            raise err.NumericGteError(value=self.constr.gte)

    def _validate_lte(self, value: Decimal):
        if value > self.constr.lte:
            raise err.NumericLteError(value=self.constr.lte)

    def _validate_gt(self, value: Decimal):
        if value <= self.constr.gt:
            raise err.NumericGtError(value=self.constr.gt)

    def _validate_lt(self, value: Decimal):
        if value >= self.constr.lt:
            raise err.NumericLtError(value=self.constr.lt)

    def transform(self, value: Decimal | None) -> Decimal | None:
        return type_transformers.transform_numeric(value, self.constr.precision, self.constr.scale)


class TimeConstraintValidator(ConstraintValidator[TimeConstraint]):
    _transform = type_transformers.transform_time

    def get_validators(self) -> Iterator[Callable]:
        if self.constr.gte is not None:
            yield self._validate_gte
        if self.constr.lte is not None:
            yield self._validate_lte

    def _validate_gte(self, value: time):
        if value < self.constr.gte:
            raise err.TimeGteError(value=self.constr.gte)

    def _validate_lte(self, value: time):
        if value > self.constr.lte:
            raise err.TimeLteError(value=self.constr.lte)


constraint_validators_map: dict[Types, Type[CONSTR_VAL]] = {
    Types.BOOLEAN: BooleanConstraintValidator,
    Types.DATE: DateConstraintValidator,
    Types.DATETIME: DateTimeConstraintValidator,
    Types.ENUM: EnumConstraintValidator,
    Types.GUID: GuidConstraintValidator,
    Types.INTEGER: IntegerConstraintValidator,
    Types.NUMERIC: NumericConstraintValidator,
    Types.STRING: StringConstraintValidator,
    Types.TEXT: StringConstraintValidator,
    Types.TIME: TimeConstraintValidator,
}


def get_constraints_validator(constraint: CONSTRAINT) -> CONSTR_VAL:
    return constraint_validators_map[constraint.type](constraint)
