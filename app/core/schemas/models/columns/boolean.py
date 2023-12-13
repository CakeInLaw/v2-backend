from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from ..._enums import ColumnTypes


__all__ = ["BooleanSchema", "BooleanSchemaGenerator"]


class BooleanSchema(ColumnSchema):
    pass


@column_schemas.dispatch_for(types.Boolean)
class BooleanSchemaGenerator(ColumnSchemaGenerator[types.Boolean, types.BooleanInfo, BooleanSchema, MODEL]):
    schema_cls = BooleanSchema
    _type = ColumnTypes.BOOLEAN
