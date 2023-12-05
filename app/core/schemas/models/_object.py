from typing import TypeVar, Any, Type

from core.db.models import OBJECT, ListModel
from ._base import ModelSchema, ModelSchemaGenerator, model_schemas
from ._schema_generator import kw_property
from .list import ListModelSchema

__all__ = ["ObjectSchema", "ObjectSchemaGenerator"]

LM = TypeVar("LM", bound=ListModelSchema)
O_SCH = TypeVar("O_SCH", bound="ObjectSchema")


class ObjectSchema(ModelSchema):
    lists: dict[str, LM]


class ObjectSchemaGenerator(ModelSchemaGenerator[O_SCH, OBJECT]):
    schema_cls: Type[O_SCH] = ObjectSchema

    @kw_property
    def lists(self):
        lists = {}
        for name, rel in self.mapper.relationships.items():
            rel_model = self._model.find_by_table(rel.target)
            if issubclass(rel_model, ListModel):
                lists[name] = model_schemas.dispatch(rel_model).schema()
        return lists
