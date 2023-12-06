from typing import Type, cast, Generic, TypeVar

import sqlalchemy as sa
from pydantic import BaseModel

from core.db.models import MODEL
from core.db.types import TypeDecorator, ColumnInfo
from .._schema_generator import BaseAttrSchemaGenerator, AttrSchemaGeneratorDispatcher, kw_property
from ..._enums import FieldTypes


__all__ = [
    "ColumnSchema", "ColumnSchemaGenerator",
    "column_schemas",
    "COL_TYPE", "COL_INFO", "C_SCH"
]


COL_TYPE = TypeVar('COL_TYPE', bound=TypeDecorator)
COL_INFO = TypeVar('COL_INFO', bound=ColumnInfo)
C_SCH = TypeVar("C_SCH", bound="ColumnSchema")
COL_GEN = TypeVar("COL_GEN", bound="ColumnSchemaGenerator")


class ColumnSchema(BaseModel):
    name: str
    type: FieldTypes
    read_only: bool
    nullable: bool
    has_default: bool

    @property
    def required(self) -> bool:
        return self.has_default or not self.nullable


class ColumnSchemaGenerator(
    BaseAttrSchemaGenerator[C_SCH, MODEL, sa.Column],
    Generic[COL_TYPE, COL_INFO, C_SCH, MODEL]
):
    _type: FieldTypes

    @property
    def _col(self):
        return self._attr

    @property
    def _col_type(self) -> COL_TYPE:
        return cast(COL_TYPE, self._col.type)

    @property
    def _col_info(self) -> COL_INFO:
        return cast(COL_INFO, self._col.info)

    @kw_property
    def name(self) -> str:
        return self._col.key

    @kw_property
    def type(self) -> FieldTypes:
        return self._type

    @kw_property
    def nullable(self) -> bool:
        return self._col.nullable

    @kw_property
    def read_only(self) -> bool:
        return self._col_info['read_only']

    @kw_property
    def has_default(self) -> bool:
        return self._col.default is not None or self._col.server_default is not None


class RelationSchemaGeneratorDispatcher(
    AttrSchemaGeneratorDispatcher[COL_GEN, Type[COL_TYPE], sa.Column]
):
    def should_reg_by_type(self, type_):
        return issubclass(type_, TypeDecorator)

    def _dispatch_by_attr(self, model: Type[MODEL], attr: sa.Column) -> Type[COL_GEN] | None:
        type_ = cast(Type[COL_TYPE], attr.type.__class__)
        return self._reg_map[type_]


column_schemas = RelationSchemaGeneratorDispatcher()
