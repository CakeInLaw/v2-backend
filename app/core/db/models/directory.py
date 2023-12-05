from typing import ClassVar, TypeVar

from ._object import Object


__all__ = ["Directory", "DIRECTORY"]


class Directory(Object):
    __abstract__ = True

    __SCHEMA__: ClassVar[str] = 'directories'


DIRECTORY = TypeVar('DIRECTORY', bound=Directory)
