from typing import TypeVar, Type

from core.db.models import Model, Document, DOCUMENT, ListModel
from ._base import model_schemas
from ._object import ObjectSchema, ObjectSchemaGenerator
from ._schema_generator import kw_property


__all__ = ["DocumentSchema", "DocumentSchemaGenerator", "collect_documents"]

DOC_SCH = TypeVar("DOC_SCH", bound="DocumentSchema")


class DocumentSchema(ObjectSchema):
    prefix: str


@model_schemas.dispatch_for(Document)
class DocumentSchemaGenerator(ObjectSchemaGenerator[DOC_SCH, DOCUMENT]):
    schema_cls: Type[DOC_SCH] = DocumentSchema

    @kw_property
    def prefix(self) -> str:
        return self._model.__PREFIX__


def collect_documents():
    models = []
    for (namespace, _), model in Model.iter_models('documents'):
        if issubclass(model, ListModel):
            # set in ObjectSchema.lists and can`t exist without owner class
            # see ._object.py
            continue
        models.append(model_schemas.dispatch(model).schema())
    return models
