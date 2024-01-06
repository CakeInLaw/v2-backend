from typing import TypeVar, TYPE_CHECKING, Type
from uuid import UUID

from sqlalchemy.orm import Mapped

from ._base import Model
from ..types import guid

if TYPE_CHECKING:
    from .list import LIST_MODEL


__all__ = ["Object", "OBJECT"]


class Object(Model):
    __abstract__ = True

    id: Mapped[UUID] = guid(primary_key=True)

    @classmethod
    def get_list_model(cls, name: str) -> Type["LIST_MODEL"]:
        return cls.find_by_table(cls.__mapper__.relationships[name].target)


OBJECT = TypeVar('OBJECT', bound=Object)
