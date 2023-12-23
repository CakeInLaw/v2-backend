from typing import Generic, Type, cast, TypeVar

from sqlalchemy import Table
from sqlalchemy.ext.hybrid import HybridExtensionType

from core.db.models import (
    MODEL, OBJECT, DIRECTORY, DOCUMENT,
    Model, Directory, Document, ListModel
)
from core.schema.models import (
    M_SCH, ModelSchema,
    O_SCH, ObjectSchema,
    DIR_SCH, DirectorySchema,
    DOC_SCH, DocumentSchema
)
from core.schema.attrs import A_SCH
from .dispatcher import model_schema_generators
from .attrs import (
    column_schema_generators,
    relation_schema_generators,
    composite_schema_generators,
    property_schema_generators,
    list_schema_generators,
)
from ..base import BaseSchemaGenerator
from ..gen_property import gen_property


__all__ = [
    "ModelSchemaGenerator", "M_GEN",
    "ObjectSchemaGenerator", "O_GEN",
    "DirectorySchemaGenerator",
    "DocumentSchemaGenerator",
]


class ModelSchemaGenerator(BaseSchemaGenerator[M_SCH], Generic[M_SCH, MODEL]):
    schema_cls = ModelSchema

    def __init__(self, model: Type[MODEL]):
        self._model = model
        self._mapper = self._model.__mapper__
        self._table = cast(Table, self._model.__table__)

    @gen_property
    def name(self) -> str:
        return self._model.__table__name__

    @gen_property
    def primary_key(self) -> str:
        return self._mapper.primary_key[0].name

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


class ObjectSchemaGenerator(ModelSchemaGenerator[O_SCH, OBJECT]):
    schema_cls = ObjectSchema

    @gen_property
    def attrs(self) -> list[A_SCH]:
        attributes: list[A_SCH] = super().attrs()
        for rel in self._mapper.relationships.values():
            rel_model = Model.find_by_table(rel.target)
            if issubclass(rel_model, ListModel):
                attributes.append(list_schema_generators.dispatch(owner=self._model, attr=rel).schema())
        return attributes


@model_schema_generators.dispatch_for(Directory)
class DirectorySchemaGenerator(ModelSchemaGenerator[DIR_SCH, DIRECTORY]):
    schema_cls = DirectorySchema


@model_schema_generators.dispatch_for(Document)
class DocumentSchemaGenerator(ModelSchemaGenerator[DOC_SCH, DOCUMENT]):
    schema_cls = DocumentSchema

    @gen_property
    def prefix(self) -> str:
        return self._model.__PREFIX__


M_GEN = TypeVar('M_GEN', bound=ModelSchemaGenerator)
O_GEN = TypeVar('O_GEN', bound=ObjectSchemaGenerator)
