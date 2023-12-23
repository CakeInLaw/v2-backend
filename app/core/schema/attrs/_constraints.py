from datetime import date, datetime, time
from decimal import Decimal
from typing import TypeVar, ClassVar

from pydantic import BaseModel

from core.settings import settings
from .._types import Types


__all__ = [
    "Constraint", "C",
    "BooleanConstraint", "DateConstraint", "DateTimeConstraint",
    "EnumConstraint", "GuidConstraint", "IntegerConstraint",
    "NumericConstraint", "StringConstraint", "TimeConstraint"
]


class Constraint(BaseModel):
    _type: ClassVar[Types]

    @property
    def type(self) -> Types:
        return self._type


C = TypeVar('C', bound=Constraint)


class BooleanConstraint(Constraint):
    _type: ClassVar[Types] = Types.BOOLEAN


class DateConstraint(Constraint):
    _type: ClassVar[Types] = Types.DATE

    gte: date | None = None
    lte: date | None = None
    fmt: str = settings.default_date_fmt


class DateTimeConstraint(Constraint):
    _type: ClassVar[Types] = Types.DATETIME

    gte: datetime | None = None
    lte: datetime | None = None
    fmt: str = settings.default_datetime_fmt
    with_timezone: bool


class EnumConstraint(Constraint):
    _type: ClassVar[Types] = Types.ENUM

    enum_type_name: str


class GuidConstraint(Constraint):
    _type: ClassVar[Types] = Types.GUID


class IntegerConstraint(Constraint):
    _type: ClassVar[Types] = Types.INTEGER

    gte: int
    lte: int


class NumericConstraint(Constraint):
    _type: ClassVar[Types] = Types.NUMERIC

    precision: int
    scale: int
    gte: Decimal | None = None
    gt: Decimal | None = None
    lte: Decimal | None = None
    lt: Decimal | None = None


class StringConstraint(Constraint):

    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None

    @property
    def type(self) -> Types:
        if self.max_length:
            return Types.STRING
        return Types.TEXT


class TimeConstraint(Constraint):
    _type: ClassVar[Types] = Types.TIME

    gte: time | None = None
    lte: time | None = None
    fmt: str = settings.default_time_fmt
