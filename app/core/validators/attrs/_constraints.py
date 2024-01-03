import re
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Generic, Callable, Iterator, TypeVar, Any, Type
from uuid import UUID

from core.schema import (
    C as CONSTRAINT, ENUM,
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

    def __init__(self, constr: CONSTRAINT):
        self.constr = constr

    def get_validators(self) -> Iterator[Callable]:
        return iter([])

    def _transform(self, value: Any) -> T:
        raise NotImplementedError

    def transform(self, value: Any) -> T | None:
        if value is None:
            return None
        value = self._transform(value=value)
        assert isinstance(value, self.constr.python_type)
        return value


CONSTR_VAL = TypeVar('CONSTR_VAL', bound=ConstraintValidator)


class BooleanConstraintValidator(ConstraintValidator[BooleanConstraint, bool]):
    BOOL_TRUE = {1, '1', 'on', 't', 'true', 'y', 'yes'}
    BOOL_FALSE = {0, '0', 'off', 'f', 'false', 'n', 'no'}

    def _transform(self, value: int | str | bool) -> bool:
        if not (value is True or value is False):
            if value in self.BOOL_TRUE:
                value = True
            elif value in self.BOOL_FALSE:
                value = False
            else:
                raise ValueError(f'Impossible to bring "{value}" to bool')
        return value


class DateConstraintValidator(ConstraintValidator[DateConstraint, date]):

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

    def _transform(self, value: str | date) -> date:
        if isinstance(value, str):
            value = date.fromisoformat(value)
        return value


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


class EnumConstraintValidator(ConstraintValidator[EnumConstraint, ENUM]):

    def _transform(self, value: str | int | ENUM) -> ENUM:
        if isinstance(value, str):
            if self.constr.is_int_enum:
                value = int(value)
            value = self.constr.python_type(value)
        elif isinstance(value, int):
            if self.constr.is_str_enum:
                value = str(value)
            value = self.constr.python_type(value)
        return value


class GuidConstraintValidator(ConstraintValidator[GuidConstraint]):
    def _transform(self, value: str | UUID) -> UUID:
        if isinstance(value, str):
            value = UUID(value)
        return value


class IntegerConstraintValidator(ConstraintValidator[IntegerConstraint]):
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

    def _transform(self, value: str | int) -> int:
        if isinstance(value, str):
            value = int(value)
        return value


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
        return Decimal(f'0.{"0" * (self.constr.scale - 1)}1')


class StringConstraintValidator(ConstraintValidator[StringConstraint]):
    _allowed_transform_types = (int, float, Decimal)

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

    def _transform(self, value: str) -> str:
        if not isinstance(value, str):
            if isinstance(value, self._allowed_transform_types):
                value = str(value)
            else:
                raise ValueError(f'Can`t convert "{value}" to str. Available types are {self._allowed_transform_types}')
        return value.strip()


class TimeConstraintValidator(ConstraintValidator[TimeConstraint]):
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

    def _transform(self, value: time | str) -> time:
        if isinstance(value, str):
            value = time.fromisoformat(value)
        return value


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
