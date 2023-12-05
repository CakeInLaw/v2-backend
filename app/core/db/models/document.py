from datetime import datetime
from typing import ClassVar, TypeVar

from sqlalchemy.orm import Mapped

from ._object import Object
from .. import types

__all__ = ["Document", "DOCUMENT"]


class Document(Object):
    __abstract__ = True

    __SCHEMA__: ClassVar[str] = 'documents'
    __PREFIX__: ClassVar[str]

    conducted: Mapped[bool] = types.boolean(default=False)
    dt: Mapped[datetime] = types.datetime(auto_now_add=True)
    comment: Mapped[str] = types.string(default='')


DOCUMENT = TypeVar('DOCUMENT', bound=Document)
