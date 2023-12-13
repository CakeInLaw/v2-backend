from typing import Type, TypeVar

from sqlalchemy.orm import CompositeProperty

from core.db.models import MODEL
from .._schema_generator import kw_property
from .._attrs import AttrSchema, AttrSchemaGenerator, AttrSchemaGeneratorDispatcher
from ..._enums import AttrTypes, CompositeTypes


__all__ = ["CompositeSchema", "CompositeSchemaGenerator", "composite_schemas", "C_SCH"]

C_SCH = TypeVar("C_SCH", bound="CompositeSchema")
C_GEN = TypeVar("C_GEN", bound="CompositeSchemaGenerator")


class CompositeSchema(AttrSchema):
    type: CompositeTypes
    attrs: list[str]


class CompositeSchemaGenerator(AttrSchemaGenerator[C_SCH, MODEL, CompositeProperty]):
    _attr_type = AttrTypes.COMPOSITE
    _type: CompositeTypes
    schema_cls: Type[C_SCH]

    @property
    def _comp(self):
        return self._attr

    @kw_property
    def name(self) -> str:
        return self._comp.key

    @kw_property
    def type(self) -> CompositeTypes:
        return self._type

    @kw_property
    def attrs(self) -> list[str]:
        return list(self._comp.attrs)


class CompositeSchemaGeneratorDispatcher(AttrSchemaGeneratorDispatcher[C_GEN, type, CompositeProperty]):

    def _dispatch_by_attr(self, model: Type[MODEL], attr: CompositeProperty) -> Type[C_GEN]:
        for base in attr.composite_class.__mro__:
            if base in self._reg_map:
                return self._reg_map[base]
        raise ValueError(f'No {model} or it`s child registered')


composite_schemas = CompositeSchemaGeneratorDispatcher()
