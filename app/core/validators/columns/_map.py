from typing import Type

from core.schemas import FieldTypes
from core.schemas.models.columns import C_SCH

from ._base import CV
from .boolean import BooleanValidator
from .date import DateValidator
from .datetime import DateTimeValidator
from .enum import EnumValidator
from .guid import GuidValidator
from .integer import IntegerValidator
from .numeric import NumericValidator
from .string import StringValidator
from .time import TimeValidator

__all__ = ["get_column_validator"]


column_validators_map: dict[FieldTypes, Type[CV]] = {
    FieldTypes.BOOLEAN: BooleanValidator,
    FieldTypes.DATE: DateValidator,
    FieldTypes.DATETIME: DateTimeValidator,
    FieldTypes.ENUM: EnumValidator,
    FieldTypes.GUID: GuidValidator,
    FieldTypes.INTEGER: IntegerValidator,
    FieldTypes.NUMERIC: NumericValidator,
    FieldTypes.STRING: StringValidator,
    FieldTypes.TEXT: StringValidator,
    FieldTypes.TIME: TimeValidator,
}


def get_column_validator(schema: C_SCH) -> CV:
    return column_validators_map[schema.type](schema)
