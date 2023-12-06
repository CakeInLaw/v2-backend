from typing import Type, cast, TypeVar

import sqlalchemy as sa
from pydantic import BaseModel

from core.db.models import MODEL
from ._schema_generator import kw_property, BaseSchemaGenerator
from .columns import ColumnSchema, column_schemas
from .relations import RelationSchema, relation_schemas
from .composite import CompositeSchema, composite_schemas


__all__ = ["ModelSchema", "M_SCH", "ModelSchemaGenerator", "model_schemas"]


COL = TypeVar("COL", bound=ColumnSchema)
REL = TypeVar("REL", bound=RelationSchema)
COMP = TypeVar("COMP", bound=CompositeSchema)
M_SCH = TypeVar("M_SCH", bound="ModelSchema")


class ModelSchema(BaseModel):
    namespace: str
    name: str
    primary_keys: list[str]
    columns: list[COL]
    relations: list[REL]
    composites: list[COMP]


class ModelSchemaGenerator(BaseSchemaGenerator[M_SCH, MODEL]):
    schema_cls = ModelSchema

    def __init__(self, model: Type[MODEL]):
        super().__init__(model=model)
        self.mapper = self._model.__mapper__
        self.table = cast(sa.Table, self._model.__table__)

    @kw_property
    def namespace(self) -> str:
        return self._model.__namespace__

    @kw_property
    def name(self) -> str:
        return self._model.__table__name__

    @kw_property
    def primary_keys(self) -> list[str]:
        return list(map(lambda pk: pk.key, self.mapper.primary_key))

    @kw_property
    def columns(self) -> list[COL]:
        return [
            column_schemas.dispatch(model=self._model, attr=col).schema()
            for col in self.mapper.columns
        ]

    @kw_property
    def relations(self) -> list[REL]:
        return [
            generator.schema()
            for rel in self.mapper.relationships.values()
            if (generator := relation_schemas.dispatch(model=self._model, attr=rel))
        ]

    @kw_property
    def composites(self) -> list[COMP]:
        return [
            composite_schemas.dispatch(model=self._model, attr=comp).schema()
            for comp in self.mapper.composites.values()
        ]


GEN = TypeVar('GEN', bound=ModelSchemaGenerator)


class ModelSchemaGeneratorDispatcher:
    def __init__(self):
        self._reg_map: dict[Type[MODEL], Type[GEN]] = {}

    def dispatch_for(self, model: Type[MODEL]):
        def registrator(gen: Type[GEN]):
            self._reg_map[model] = gen
            return gen
        return registrator

    def dispatch(self, model: Type[MODEL]) -> Type[GEN]:
        for base in model.__mro__:
            if base in self._reg_map:
                base = cast(Type[MODEL], base)
                return self._reg_map[base](model)
        raise Exception(f'No {model} or it`s child registered')


model_schemas = ModelSchemaGeneratorDispatcher()
