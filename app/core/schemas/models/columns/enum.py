from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import FieldTypes


__all__ = ["EnumSchema", "DateTimeSchemaGenerator"]


class EnumSchema(ColumnSchema):
    enum_type_name: str


@column_schemas.dispatch_for(types.Enum)
class DateTimeSchemaGenerator(ColumnSchemaGenerator[types.Enum, types.EnumInfo, EnumSchema, MODEL]):
    _type = FieldTypes.ENUM
    schema_cls = EnumSchema

    @kw_property
    def enum_type_name(self) -> str:
        return self._col_type.enum_type.__name__
