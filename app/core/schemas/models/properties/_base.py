from typing import Type, cast, TypeVar

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property

from core.db.models import MODEL
from .._schema_generator import kw_property
from .._attrs import AttrSchema, AttrSchemaGenerator, AttrSchemaGeneratorDispatcher
from ..._enums import AttrTypes, ColumnTypes


__all__ = [
    "PropertySchema", "PropertySchemaGenerator",
]


P_SCH = TypeVar('P_SCH', bound="ColumnSchema")


class PropertySchema(AttrSchema):
    required: bool
    getter: dict
    setter: dict


class PropertySchemaGenerator(AttrSchemaGenerator[P_SCH, MODEL, hybrid_property]):
    _attr_type = AttrTypes.PROPERTY

    @kw_property
    def name(self) -> str:
        return self._attr.__name__

    @kw_property
    def required(self) -> bool:
        return self._attr.info['required']

    @kw_property
    def getter(self) -> ...:
        pass

    @kw_property
    def setter(self) -> ...:
        pass


class PropertySchemaDispatcher:
    def dispatch_for(self, type_):
        pass

    def dispatch(self, type_):
        pass
