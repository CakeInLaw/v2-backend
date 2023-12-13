from datetime import datetime

from core.db import types
from core.db.models import MODEL
from ._base import ColumnSchema, ColumnSchemaGenerator, column_schemas
from .._schema_generator import kw_property
from ..._enums import ColumnTypes


__all__ = ["DateTimeSchema", "DateTimeSchemaGenerator"]


class DateTimeSchema(ColumnSchema):
    gte: datetime | None
    lte: datetime | None
    fmt: str
    with_timezone: bool


@column_schemas.dispatch_for(types.DateTime)
class DateTimeSchemaGenerator(ColumnSchemaGenerator[types.DateTime, types.DateTimeInfo, DateTimeSchema, MODEL]):
    schema_cls = DateTimeSchema
    _type = ColumnTypes.DATETIME

    @kw_property
    def gte(self) -> datetime | None:
        return self._col_type.gte

    @kw_property
    def lte(self) -> datetime | None:
        return self._col_type.lte

    @kw_property
    def fmt(self) -> str:
        return self._col_info['fmt']

    @kw_property
    def with_timezone(self) -> bool:
        return self._col_type.timezone
