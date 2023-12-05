from decimal import Decimal

from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import FieldTypes


__all__ = ["NumericSchema", "NumericSchemaGenerator"]


class NumericSchema(ColumnSchema):
    precision: int
    scale: int
    gte: Decimal | None
    gt: Decimal | None
    lte: Decimal | None
    lt: Decimal | None


@column_schemas.dispatch_for(types.Numeric)
class NumericSchemaGenerator(ColumnSchemaGenerator[types.Numeric, types.NumericInfo, NumericSchema, MODEL]):
    schema_cls = NumericSchema
    _type = FieldTypes.NUMERIC

    @kw_property
    def precision(self) -> int:
        return self._col_type.precision

    @kw_property
    def scale(self) -> int:
        return self._col_type.scale

    @kw_property
    def gte(self) -> Decimal | None:
        return self._col_type.gte

    @kw_property
    def gt(self) -> Decimal | None:
        return self._col_type.gt

    @kw_property
    def lte(self) -> Decimal | None:
        return self._col_type.lte

    @kw_property
    def lt(self) -> Decimal | None:
        return self._col_type.lt
