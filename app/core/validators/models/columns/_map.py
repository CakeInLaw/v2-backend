from typing import Type, TYPE_CHECKING

from core.schemas import ColumnTypes
from core.schemas.models.columns import C_SCH

from ._base import COL_VAL
from .boolean import BooleanValidator
from .date import DateValidator
from .datetime import DateTimeValidator
from .enum import EnumValidator
from .guid import GuidValidator
from .integer import IntegerValidator
from .numeric import NumericValidator
from .string import StringValidator
from .time import TimeValidator

if TYPE_CHECKING:
    from .._base import M_VAL


__all__ = ["get_column_validator"]


column_validators_map: dict[ColumnTypes, Type[COL_VAL]] = {
    ColumnTypes.BOOLEAN: BooleanValidator,
    ColumnTypes.DATE: DateValidator,
    ColumnTypes.DATETIME: DateTimeValidator,
    ColumnTypes.ENUM: EnumValidator,
    ColumnTypes.GUID: GuidValidator,
    ColumnTypes.INTEGER: IntegerValidator,
    ColumnTypes.NUMERIC: NumericValidator,
    ColumnTypes.STRING: StringValidator,
    ColumnTypes.TEXT: StringValidator,
    ColumnTypes.TIME: TimeValidator,
}


def get_column_validator(schema: C_SCH, model_validator: Type["M_VAL"]) -> COL_VAL:
    return column_validators_map[schema.type](schema, model_validator)
