from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from ..._enums import FieldTypes


__all__ = ["GuidSchema", "GuidSchemaGenerator"]


class GuidSchema(ColumnSchema):
    pass


@column_schemas.dispatch_for(types.Guid)
class GuidSchemaGenerator(ColumnSchemaGenerator[types.Guid, types.GuidInfo, GuidSchema, MODEL]):
    schema_cls = GuidSchema
    _type = FieldTypes.GUID
