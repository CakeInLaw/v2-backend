from typing import Any, Type

from sqlalchemy import select

from core.types import PK
from core.db import OBJECT, DIRECTORY, DOCUMENT
from core.db.connection import AsyncSession
from core.schema import O_SCH, DIR_SCH, DOC_SCH, get_default_app_schema
from core.validators import ObjectValidator, O_VAL, DirectoryValidator, DIR_VAL, DocumentValidator, DOC_VAL
from .lists import SaListRepository
from .._base import AbstractObjectRepository, O_REP
from ..exceptions import ObjectNotFoundError


__all__ = ["SaObjectRepository", "SaDirectoryRepository", "SaDocumentRepository"]



class SaObjectRepository(AbstractObjectRepository[OBJECT, O_SCH, O_VAL]):
    validator_cls = ObjectValidator
    DEFAULT_LIST_REPOSITORY_CLS = SaListRepository

    def __init__(self, context: dict[str, Any]):
        super().__init__(context=context)
        self.session: AsyncSession = self.context['session']

    @classmethod
    def _get_list_model(cls, name: str) -> Any:
        return cls.model.get_list_model(name)

    @classmethod
    def bind_schema_automatically(cls: Type["O_REP"]) -> Type["O_REP"]:
        return cls.bind_schema(schema=cls._find_schema())

    @classmethod
    def _find_schema(cls) -> O_SCH: ...

    def get_pk_attr(self):
        return getattr(self.model, self.schema.primary_key)

    async def get(self, **kwargs): ...

    async def get_many(self, pks: list[PK], **kwargs) -> dict[PK, OBJECT]:

    async def get_one(self, pk: PK, raise_if_none: bool = True, **kwargs) -> OBJECT | None:
        result = await self.session.scalar(select(self.model).where(self.get_pk_attr() == pk))
        if result is None and raise_if_none:
            raise ObjectNotFoundError
        return result


class SaDirectoryRepository(SaObjectRepository[DIRECTORY, DIR_SCH, DIR_VAL]):
    validator_cls = DirectoryValidator

    @classmethod
    def _find_schema(cls) -> DIR_SCH:
        return get_default_app_schema().get_directory(cls.model.__table__name__)

    async def conduct(self) -> None:
        raise Exception('Can`t exec conduct. Available only for Document')


class SaDocumentRepository(SaObjectRepository[DOCUMENT, DOC_SCH, DOC_VAL]):
    validator_cls = DocumentValidator

    @classmethod
    def _find_schema(cls) -> DIR_SCH:
        return get_default_app_schema().get_document(cls.model.__table__name__)

    async def conduct(self) -> None:
        assert self.instance
        ...
