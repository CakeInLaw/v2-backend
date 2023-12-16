from typing import Generic, Type, cast, TypeVar

from sqlalchemy import Table

from core.db.models import (
    MODEL, OBJECT, DIRECTORY, DOCUMENT,
    Directory, Document
)
from core.schema.models import (
    M_SCH, ModelSchema,
    O_SCH, ObjectSchema,
    DIR_SCH, DirectorySchema,
    DOC_SCH, DocumentSchema
)
from .dispatcher import model_schema_generators
from ..base import BaseSchemaGenerator
from ..gen_property import gen_property
from ...schema.attrs import A_SCH


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
    def namespace(self) -> str:
        return self._model.__namespace__

    @gen_property
    def name(self) -> str:
        return self._model.__table__name__

    @gen_property
    def primary_key(self) -> str:
        return self._mapper.primary_key[0].name

    @gen_property
    def attrs(self) -> list[A_SCH]:
        pass


class ObjectSchemaGenerator(ModelSchemaGenerator[O_SCH, OBJECT]):
    schema_cls = ObjectSchema


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
