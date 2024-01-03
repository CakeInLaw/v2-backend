import enum
import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import TypeVar, ClassVar, Type

from pydantic import BaseModel

from core import utils
from core.settings import settings
from .._types import Types


__all__ = [
    "Constraint", "C", "ENUM",
    "BooleanConstraint", "DateConstraint", "DateTimeConstraint",
    "EnumConstraint", "GuidConstraint", "IntegerConstraint",
    "NumericConstraint", "StringConstraint", "TimeConstraint"
]


class Constraint(BaseModel):
    _python_type: ClassVar[type]
    _type: ClassVar[Types]

    @property
    def python_type(self) -> type:
        return self._python_type

    @property
    def type(self) -> Types:
        return self._type


C = TypeVar('C', bound=Constraint)


class BooleanConstraint(Constraint):
    _python_type: ClassVar = bool
    _type: ClassVar[Types] = Types.BOOLEAN


class DateConstraint(Constraint):
    _python_type: ClassVar = date
    _type: ClassVar[Types] = Types.DATE

    gte: date | None = None
    lte: date | None = None
    fmt: str = settings.default_date_fmt


class DateTimeConstraint(Constraint):
    _python_type: ClassVar = datetime
    _type: ClassVar[Types] = Types.DATETIME

    gte: datetime | None = None
    lte: datetime | None = None
    fmt: str = settings.default_datetime_fmt
    with_timezone: bool


ENUM = TypeVar('ENUM', enum.IntEnum, enum.StrEnum)


class EnumConstraint(Constraint):
    _type: ClassVar[Types] = Types.ENUM

    enum_type_name: str

    @property
    def python_type(self) -> Type[ENUM]:
        if not hasattr(self, "_python_type_cached"):
            setattr(self, "_python_type_cached", utils.import_string(f'enums.{self.enum_type_name}'))
        return getattr(self, "_python_type_cached")

    @property
    def is_int_enum(self) -> bool:
        if not hasattr(self, "_is_int_enum_cached"):
            setattr(self, "_is_int_enum_cached", issubclass(self.python_type, enum.IntEnum))
        return hasattr(self, "_is_int_enum_cached")

    @property
    def is_str_enum(self) -> bool:
        if not hasattr(self, "_is_str_enum_cached"):
            setattr(self, "_is_str_enum_cached", issubclass(self.python_type, enum.StrEnum))
        return hasattr(self, "_is_str_enum_cached")


class GuidConstraint(Constraint):
    _python_type: ClassVar = uuid.UUID
    _type: ClassVar[Types] = Types.GUID


class IntegerConstraint(Constraint):
    _python_type: ClassVar = int
    _type: ClassVar[Types] = Types.INTEGER

    gte: int
    lte: int


class NumericConstraint(Constraint):
    _python_type: ClassVar = Decimal
    _type: ClassVar[Types] = Types.NUMERIC

    precision: int
    scale: int
    gte: Decimal | None = None
    gt: Decimal | None = None
    lte: Decimal | None = None
    lt: Decimal | None = None


class StringConstraint(Constraint):
    _python_type: ClassVar = str

    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None

    @property
    def type(self) -> Types:
        if self.max_length:
            return Types.STRING
        return Types.TEXT


class TimeConstraint(Constraint):
    _python_type: ClassVar = time
    _type: ClassVar[Types] = Types.TIME

    gte: time | None = None
    lte: time | None = None
    fmt: str = settings.default_time_fmt
