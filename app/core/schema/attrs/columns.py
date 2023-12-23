from typing import Generic, TypeVar, ClassVar

from pydantic import computed_field

from .._types import Attrs, Types
from ._base import AttrSchema
from . import _constraints as constr
from ._constraints import C


__all__ = [
    "ColumnSchema", "COL_SCH",
    "BooleanSchema", "DateSchema", "DateTimeSchema",
    "EnumSchema", "GuidSchema", "IntegerSchema",
    "NumericSchema", "StringSchema", "TimeSchema",
]


class ColumnSchema(AttrSchema, Generic[C]):
    _attr: ClassVar[Attrs] = Attrs.COLUMN

    read_only: bool
    hidden: bool
    nullable: bool
    has_default: bool
    unique: bool
    constraints: C

    @computed_field
    @property
    def type(self) -> Types:
        return self.constraints.type


COL_SCH = TypeVar('COL_SCH', bound=ColumnSchema)


BooleanSchema = ColumnSchema[constr.BooleanConstraint]
DateSchema = ColumnSchema[constr.DateConstraint]
DateTimeSchema = ColumnSchema[constr.DateTimeConstraint]
EnumSchema = ColumnSchema[constr.EnumConstraint]
GuidSchema = ColumnSchema[constr.GuidConstraint]
IntegerSchema = ColumnSchema[constr.IntegerConstraint]
NumericSchema = ColumnSchema[constr.NumericConstraint]
StringSchema = ColumnSchema[constr.StringConstraint]
TimeSchema = ColumnSchema[constr.TimeConstrain]
