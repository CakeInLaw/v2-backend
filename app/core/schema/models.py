from typing import TypeVar

from pydantic import BaseModel, InstanceOf

from .attrs import AttrSchema


__all__ = [
    "ModelSchema", "ObjectSchema", "DirectorySchema", "DocumentSchema",
    "M_SCH", "O_SCH", "DIR_SCH", "DOC_SCH"
]


class ModelSchema(BaseModel):
    namespace: str
    name: str
    primary_key: str
    attrs: list[InstanceOf[AttrSchema]]


class ObjectSchema(ModelSchema):
    pass


class DirectorySchema(ObjectSchema):
    pass


class DocumentSchema(ObjectSchema):
    prefix: str


M_SCH = TypeVar('M_SCH', bound=ModelSchema)
O_SCH = TypeVar('O_SCH', bound=ObjectSchema)
DIR_SCH = TypeVar('DIR_SCH', bound=DirectorySchema)
DOC_SCH = TypeVar('DOC_SCH', bound=DocumentSchema)
