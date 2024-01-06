from typing import Any, Type

from core.db import OBJECT, DIRECTORY, DOCUMENT
from core.schema import O_SCH, DIR_SCH, DOC_SCH, get_default_app_schema
from core.validators import ObjectValidator, O_VAL, DirectoryValidator, DIR_VAL, DocumentValidator, DOC_VAL
from .._base import AbstractObjectRepository, O_REP
from .lists import SaListRepository


__all__ = ["SaObjectRepository", "SaDirectoryRepository", "SaDocumentRepository"]


class SaObjectRepository(AbstractObjectRepository[OBJECT, O_SCH, O_VAL]):
    validator_cls = ObjectValidator
    DEFAULT_LIST_REPOSITORY_CLS = SaListRepository

    def __init__(self, context: dict[str, Any]):
        super().__init__(context=context)
        self.session = self.context['session']

    @classmethod
    def _get_list_model(cls, name: str) -> Any:
        return cls.model.get_list_model(name)

    @classmethod
    def bind_schema_automatically(cls: Type["O_REP"]) -> Type["O_REP"]:
        return cls.bind_schema(schema=cls._find_schema())

    @classmethod
    def _find_schema(cls) -> O_SCH: ...

    async def get(self):


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
