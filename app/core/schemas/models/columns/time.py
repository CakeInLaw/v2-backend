from datetime import time

from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import ColumnTypes


__all__ = ["TimeSchema", "TimeSchemaGenerator"]


class TimeSchema(ColumnSchema):
    gte: time | None
    lte: time | None
    fmt: str


@column_schemas.dispatch_for(types.Time)
class TimeSchemaGenerator(ColumnSchemaGenerator[types.Time, types.TimeInfo, TimeSchema, MODEL]):
    schema_cls = TimeSchema
    _type = ColumnTypes.TIME

    @kw_property
    def gte(self) -> time | None:
        return self._col_type.gte

    @kw_property
    def lte(self) -> time | None:
        return self._col_type.lte

    @kw_property
    def fmt(self) -> str:
        return self._col_info['fmt']
