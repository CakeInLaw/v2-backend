from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import FieldTypes


__all__ = ["IntegerSchema", "IntegerSchemaGenerator"]


class IntegerSchema(ColumnSchema):
    gte: int
    lte: int


@column_schemas.dispatch_for(types.SmallInteger)
@column_schemas.dispatch_for(types.Integer)
@column_schemas.dispatch_for(types.BigInteger)
class IntegerSchemaGenerator(ColumnSchemaGenerator[types.Integer, types.IntegerInfo, IntegerSchema, MODEL]):
    schema_cls = IntegerSchema
    _type = FieldTypes.INTEGER

    @kw_property
    def gte(self) -> int:
        return self._col_type.gte

    @kw_property
    def lte(self) -> int:
        return self._col_type.lte
