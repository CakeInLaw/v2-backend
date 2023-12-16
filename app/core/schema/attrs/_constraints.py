from datetime import date, datetime, time
from decimal import Decimal
from typing import TypeVar, ClassVar

from pydantic import BaseModel

from .._types import Types


__all__ = [
    "Constraint", "C",
    "BooleanConstraint", "DateConstraint", "DateTimeConstraint",
    "EnumConstraint", "GuidConstraint", "IntegerConstraint",
    "NumericConstraint", "StringConstraint", "TimeConstrain"
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

    gte: date | None
    lte: date | None
    fmt: str


class DateTimeConstraint(Constraint):
    _type: ClassVar[Types] = Types.DATETIME

    gte: datetime | None
    lte: datetime | None
    fmt: str
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
    gte: Decimal | None
    gt: Decimal | None
    lte: Decimal | None
    lt: Decimal | None


class StringConstraint(Constraint):

    min_length: int | None
    max_length: int | None
    pattern: str | None

    @property
    def type(self) -> Types:
        if self.max_length:
            return Types.STRING
        return Types.TEXT


class TimeConstrain(Constraint):
    _type: ClassVar[Types] = Types.TIME

    gte: time | None
    lte: time | None
    fmt: str
