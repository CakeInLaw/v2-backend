from typing import TypeVar
from uuid import UUID

from sqlalchemy.orm import Mapped

from ._base import Model
from ..types import guid


__all__ = ["Object", "OBJECT"]


class Object(Model):
    __abstract__ = True

    id: Mapped[UUID] = guid(primary_key=True)


OBJECT = TypeVar('OBJECT', bound=Object)
