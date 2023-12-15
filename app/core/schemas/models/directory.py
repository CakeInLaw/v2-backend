from typing import TypeVar, Type

from core.db.models import Model, Directory, DIRECTORY, ListModel
from ._base import model_schemas
from ._object import ObjectSchema, ObjectSchemaGenerator


__all__ = ["DirectorySchema", "DirectorySchemaGenerator", "collect_directories"]


DIR_SCH = TypeVar("DIR_SCH", bound="DirectorySchema")


class DirectorySchema(ObjectSchema):
    pass


@model_schemas.dispatch_for(Directory)
class DirectorySchemaGenerator(ObjectSchemaGenerator[DIR_SCH, DIRECTORY]):
    schema_cls: Type[DIR_SCH] = DirectorySchema


def collect_directories():
    models = []
    for (namespace, _), model in Model.iter_models('directories'):
        if issubclass(model, ListModel):
            # set in ObjectSchema.lists and can`t exist without owner class
            # see ._object.py
            continue
        models.append(model_schemas.dispatch(model).schema())
    return models
