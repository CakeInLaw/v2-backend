from typing import Type, TypeVar, cast, Generic, Any

import sqlalchemy as sa

from core.db.types import (
    COL_TYPE, COL_INFO,
    Boolean, BooleanInfo, Date, DateInfo, DateTime, DateTimeInfo,
    Enum, EnumInfo, Guid, GuidInfo, Integer, SmallInteger, BigInteger, IntegerInfo,
    Numeric, NumericInfo, String, StringInfo, Time, TimeInfo,
)
from core.db.models import MODEL
from core.schema.attrs import (
    ColumnSchema, COL_SCH,
    BooleanSchema, DateSchema, DateTimeSchema,
    EnumSchema, GuidSchema, IntegerSchema,
    NumericSchema, StringSchema, TimeSchema,
)
from ._base import AttrSchemaGenerator
from ._dispatcher import AttrSchemaGeneratorDispatcher
from ... import gen_property


__all__ = [
    "ColumnSchemaGenerator", "COL_GEN", "column_schema_generators",
    "BooleanSchemaGenerator", "DateSchemaGenerator", "DateTimeSchemaGenerator",
    "EnumSchemaGenerator", "GuidSchemaGenerator", "IntegerSchemaGenerator",
    "NumericSchemaGenerator", "StringSchemaGenerator", "TimeSchemaGenerator",
]


class ColumnSchemaGenerator(AttrSchemaGenerator[COL_SCH, sa.Column], Generic[COL_SCH, COL_TYPE, COL_INFO]):
    schema_cls: Type[COL_SCH] = ColumnSchema

    @property
    def _col(self):
        return self._attr

    @property
    def _col_type(self) -> COL_TYPE:
        return cast(COL_TYPE, self._col.type)

    @property
    def _col_info(self) -> COL_INFO:
        return cast(COL_INFO, self._col.info)

    @gen_property
    def name(self) -> str:
        return self._col.key

    @gen_property
    def read_only(self) -> bool:
        return self._col_info['read_only']

    @gen_property
    def hidden(self) -> bool:
        return self._col_info['hidden']

    @gen_property
    def nullable(self) -> bool:
        return self._col.nullable

    @gen_property
    def has_default(self) -> bool:
        return self._col.default is not None or self._col.server_default is not None

    @gen_property
    def unique(self) -> bool:
        return bool(self._col.unique) or self._col.primary_key

    @gen_property
    def constraints(self) -> dict[str, Any]:
        raise NotImplementedError


COL_GEN = TypeVar('COL_GEN', bound=ColumnSchemaGenerator)


class ColumnSchemaGeneratorDispatcher(AttrSchemaGeneratorDispatcher[COL_GEN, Type[COL_TYPE], sa.Column]):
    def _dispatch_by_attr(self, model: Type[MODEL], attr: sa.Column) -> Type[COL_GEN] | None:
        return self._reg_map[cast(Type[COL_TYPE], attr.type.__class__)]


column_schema_generators = ColumnSchemaGeneratorDispatcher()


@column_schema_generators.dispatch_for(Boolean)
class BooleanSchemaGenerator(ColumnSchemaGenerator[BooleanSchema, Boolean, BooleanInfo]):
    schema_cls = BooleanSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {}


@column_schema_generators.dispatch_for(Date)
class DateSchemaGenerator(ColumnSchemaGenerator[DateSchema, Date, DateInfo]):
    schema_cls = DateSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'gte': self._col_type.gte,
            'lte': self._col_type.lte,
            'fmt': self._col_info['fmt'],
        }


@column_schema_generators.dispatch_for(DateTime)
class DateTimeSchemaGenerator(ColumnSchemaGenerator[DateTimeSchema, DateTime, DateTimeInfo]):
    schema_cls = DateTimeSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'gte': self._col_type.gte,
            'lte': self._col_type.lte,
            'fmt': self._col_info['fmt'],
            'with_timezone': self._col_type.timezone,
        }


@column_schema_generators.dispatch_for(Enum)
class EnumSchemaGenerator(ColumnSchemaGenerator[EnumSchema, Enum, EnumInfo]):
    schema_cls = EnumSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'enum_type_name': self._col_type.enum_type.__name__
        }


@column_schema_generators.dispatch_for(Guid)
class GuidSchemaGenerator(ColumnSchemaGenerator[GuidSchema, Guid, GuidInfo]):
    schema_cls = GuidSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {}


@column_schema_generators.dispatch_for(SmallInteger)
@column_schema_generators.dispatch_for(Integer)
@column_schema_generators.dispatch_for(BigInteger)
class IntegerSchemaGenerator(ColumnSchemaGenerator[IntegerSchema, Integer, IntegerInfo]):
    schema_cls = IntegerSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'gte': self._col_type.gte,
            'lte': self._col_type.lte
        }


@column_schema_generators.dispatch_for(Numeric)
class NumericSchemaGenerator(ColumnSchemaGenerator[NumericSchema, Numeric, NumericInfo]):
    schema_cls = NumericSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'precision': self._col_type.precision,
            'scale': self._col_type.scale,
            'gte': self._col_type.gte,
            'gt': self._col_type.gt,
            'lte': self._col_type.lte,
            'lt': self._col_type.lt,
        }


@column_schema_generators.dispatch_for(String)
class StringSchemaGenerator(ColumnSchemaGenerator[StringSchema, String, StringInfo]):
    schema_cls = StringSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'min_length': self._col_type.min_length,
            'max_length': self._col_type.max_length,
            'pattern': self._col_info['pattern'],
        }


@column_schema_generators.dispatch_for(Time)
class TimeSchemaGenerator(ColumnSchemaGenerator[TimeSchema, Time, TimeInfo]):
    schema_cls = TimeSchema

    @gen_property
    def constraints(self) -> dict[str, Any]:
        return {
            'gte': self._col_type.gte,
            'lte': self._col_type.lte,
            'fmt': self._col_info['fmt'],
        }
