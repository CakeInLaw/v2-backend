from typing import TypeVar, Type

from core.db.models import ListModel, LIST_MODEL
from ._base import ModelSchema, ModelSchemaGenerator, model_schemas


__all__ = ["ListModelSchema", "ListModelSchemaGenerator"]

from ._schema_generator import kw_property

LM_SCH = TypeVar("LM_SCH", bound="ListModelSchema")


class ListModelSchema(ModelSchema):
    owner: str
    owner_attr_name: str


@model_schemas.dispatch_for(ListModel)
class ListModelSchemaGenerator(ModelSchemaGenerator[LM_SCH, LIST_MODEL]):
    schema_cls: Type[LM_SCH] = ListModelSchema

    @kw_property
    def owner(self) -> str:
        return self._model.__OWNER__.__full_name__

    @kw_property
    def owner_attr_name(self) -> str:
        return self._model.__BACK_POPULATES__
