from typing import Type, TypeVar

from sqlalchemy.ext.hybrid import HybridExtensionType
from sqlalchemy.orm import RelationshipProperty

from core.db.models import Model, ListModel, MODEL, LIST_MODEL
from core.schema.attrs import LIST_SCH, ListSchema, A_SCH
from .columns import column_schema_generators
from .relations import relation_schema_generators
from .composites import composite_schema_generators
from .properties import property_schema_generators
from ._base import AttrSchemaGenerator
from ._dispatcher import AttrSchemaGeneratorDispatcher
from ...gen_property import gen_property


__all__ = [
    "ListSchemaGenerator", "LIST_GEN",
    "ListSchemaGeneratorDispatcher", "list_schema_generators",
]


class ListSchemaGenerator(AttrSchemaGenerator[LIST_SCH, RelationshipProperty]):
    schema_cls = ListSchema

    def __init__(self, owner: Type[MODEL], attr: RelationshipProperty):
        super().__init__(owner=owner, attr=attr)
        list_model = Model.find_by_table(self._attr.target)
        assert issubclass(list_model, ListModel)
        self._model = list_model
        self._mapper = self._model.__mapper__

    @gen_property
    def name(self) -> str:
        return self._model.__BACK_POPULATES__

    @gen_property
    def attrs(self) -> list[A_SCH]:
        attributes: list[A_SCH] = []
        for col in self._mapper.columns:
            attributes.append(column_schema_generators.dispatch(owner=self._model, attr=col).schema())
        for rel in self._mapper.relationships.values():
            if generator := relation_schema_generators.dispatch(owner=self._model, attr=rel):
                attributes.append(generator.schema())
        for comp in self._mapper.composites.values():
            attributes.append(composite_schema_generators.dispatch(owner=self._model, attr=comp).schema())
        for prop in self._mapper.all_orm_descriptors:  # type: ignore
            if prop.extension_type == HybridExtensionType.HYBRID_PROPERTY:
                attributes.append(property_schema_generators.dispatch(owner=self._model, attr=prop).schema())
        return attributes


LIST_GEN = TypeVar('LIST_GEN', bound=ListSchemaGenerator)


class ListSchemaGeneratorDispatcher(AttrSchemaGeneratorDispatcher[LIST_GEN, Type[LIST_MODEL], RelationshipProperty]):
    def should_reg_by_type(self, type_: Type[LIST_MODEL] | Type[MODEL]):
        return issubclass(type_, ListModel)

    def _dispatch_by_attr(self, model: Type[MODEL], attr: RelationshipProperty) -> Type[LIST_GEN] | None:
        for base in Model.find_by_table(attr.target, raise_if_none=True).__mro__:
            if base in self._reg_map:
                return self._reg_map[base]
            raise ValueError(f'No {model} or it`s parent registered')


list_schema_generators = ListSchemaGeneratorDispatcher()

list_schema_generators.dispatch_for(ListModel)(ListSchemaGenerator)
