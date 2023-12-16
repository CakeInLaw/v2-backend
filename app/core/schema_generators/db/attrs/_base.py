from typing import Generic, TypeVar, Type

from core.db.models import MODEL
from core.schema.attrs import A_SCH, AttrSchema
from ...base import BaseSchemaGenerator
from ...gen_property import gen_property

ATTR = TypeVar('ATTR')


class AttrSchemaGenerator(BaseSchemaGenerator[A_SCH], Generic[A_SCH, ATTR]):
    schema_cls: Type[A_SCH] = AttrSchema

    def __init__(self, owner: Type[MODEL], attr: ATTR):
        self._owner = owner
        self._attr = attr

    @gen_property
    def name(self) -> str:
        raise NotImplementedError

    @gen_property
    def owner(self) -> str:
        return self._owner.__full_name__


ATTR_GEN = TypeVar('ATTR_GEN', bound=AttrSchemaGenerator)
