from datetime import date

from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import ColumnTypes


__all__ = ["DateSchema", "DateSchemaGenerator"]


class DateSchema(ColumnSchema):
    gte: date | None
    lte: date | None
    fmt: str


@column_schemas.dispatch_for(types.Date)
class DateSchemaGenerator(ColumnSchemaGenerator[types.Date, types.DateInfo, DateSchema, MODEL]):
    schema_cls = DateSchema
    _type = ColumnTypes.DATE

    @kw_property
    def gte(self) -> date | None:
        return self._col_type.gte

    @kw_property
    def lte(self) -> date | None:
        return self._col_type.lte

    @kw_property
    def fmt(self) -> str:
        return self._col_info['fmt']
