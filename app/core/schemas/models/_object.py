from typing import TypeVar, Type

from core.db.models import OBJECT, ListModel, Model
from ._base import ModelSchema, ModelSchemaGenerator, model_schemas
from ._schema_generator import kw_property
from .list import ListModelSchema

__all__ = ["ObjectSchema", "ObjectSchemaGenerator", "O_SCH"]


LM = TypeVar("LM", bound=ListModelSchema)
O_SCH = TypeVar("O_SCH", bound="ObjectSchema")


class ObjectSchema(ModelSchema):
    lists: list[LM]


class ObjectSchemaGenerator(ModelSchemaGenerator[O_SCH, OBJECT]):
    schema_cls: Type[O_SCH] = ObjectSchema

    @kw_property
    def lists(self):
        lists = []
        for _, rel in self.mapper.relationships.items():
            rel_model = Model.find_by_table(rel.target)
            if issubclass(rel_model, ListModel):
                lists.append(model_schemas.dispatch(rel_model).schema())
        return lists
