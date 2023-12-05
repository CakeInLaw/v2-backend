from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import FieldTypes


__all__ = ["StringSchema", "StringSchemaGenerator"]


class StringSchema(ColumnSchema):
    min_length: int | None
    max_length: int | None
    pattern: str | None


@column_schemas.dispatch_for(types.String)
class StringSchemaGenerator(ColumnSchemaGenerator[types.String, types.StringInfo, StringSchema, MODEL]):
    schema_cls = StringSchema

    @kw_property
    def type(self) -> FieldTypes:
        return FieldTypes.TEXT if self.max_length is None else FieldTypes.STRING

    @kw_property
    def min_length(self) -> int | None:
        return self._col_type.min_length

    @kw_property
    def max_length(self) -> int | None:
        return self._col_type.max_length

    @kw_property
    def pattern(self) -> str | None:
        return self._col_info['pattern']
