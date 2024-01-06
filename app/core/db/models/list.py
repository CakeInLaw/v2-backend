from typing import Type, ClassVar, TypeVar, Generic

from sqlalchemy import inspect
from sqlalchemy.orm import Mapped, declared_attr, relationship

from core.types import PK
from ._base import Model
from ._object import OBJECT
from ..relations import foreign_key
from ..types import integer


__all__ = ["ListModel", "LIST_MODEL"]


class ListModel(Model, Generic[OBJECT, PK]):
    __abstract__ = True

    __OWNER__: Type[OBJECT]
    __BACK_POPULATES__: ClassVar[str]

    rn: Mapped[int] = integer(primary_key=True, t='small')

    @declared_attr
    @classmethod
    def __tablename__(cls):
        return cls.__OWNER__.__tablename__ + '__' + super().__tablename__

    @classmethod
    def _get_schema_name(cls) -> str:
        return cls.__OWNER__._get_schema_name()

    @declared_attr
    @classmethod
    def owner_id(cls) -> Mapped[PK]:
        assert len(inspect(cls.__OWNER__).primary_key) == 1
        return foreign_key(
            inspect(cls.__OWNER__).primary_key[0],
            ondelete='CASCADE',
            primary_key=True,
            no_relation=True
        )

    @declared_attr
    @classmethod
    def owner(cls) -> Mapped[OBJECT]:
        return relationship(
            cls.__OWNER__,
            foreign_keys=[cls.owner_id],
            back_populates=cls.__BACK_POPULATES__,
            cascade='all',
        )


LIST_MODEL = TypeVar('LIST_MODEL', bound=ListModel)
