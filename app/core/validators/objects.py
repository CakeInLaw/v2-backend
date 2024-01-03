from typing import Any, TYPE_CHECKING, Type, TypeVar

from core.schema import O_SCH, DIR_SCH, DOC_SCH
from .lists import ListValidator
from .models import ModelValidatorMeta, ModelValidator

if TYPE_CHECKING:
    from core.repositories import O_REP


__all__ = [
    "ObjectValidatorMeta", "ObjectValidator", "O_VAL",
    "DirectoryValidator", "DIR_VAL",
    "DocumentValidator", "DOC_VAL",
]


class ObjectValidatorMeta(ModelValidatorMeta):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_cls = super().__new__(mcs, name, bases, attrs)
        if 'schema' not in attrs:
            return new_cls

        new_cls._lists = {
            list_schema.name: ListValidator.bind(schema=list_schema)
            for list_schema in new_cls.schema.get_lists()
        }

        return new_cls


class ObjectValidator(ModelValidator[O_SCH], metaclass=ObjectValidatorMeta):
    _lists: dict[str, "ListValidator"]
    # def get_list():

    def __init__(self, repository: "O_REP"):
        self.repository = repository

    @classmethod
    def bind(cls: Type["O_VAL"], schema: O_SCH) -> Type["O_VAL"]:
        if hasattr(cls, 'schema'):
            raise Exception(f'{cls} is already bound')
        return type(f'{schema.name}{cls.__name__}', (cls, ), {'schema': schema})  # type: ignore

    async def validate(self, data: dict[str, Any], repository: "O_REP") -> dict[str, Any]:
        pass


O_VAL = TypeVar('O_VAL', bound=ObjectValidator)


class DirectoryValidator(ObjectValidator[DIR_SCH]):
    pass


DIR_VAL = TypeVar('DIR_VAL', bound=DirectoryValidator)


class DocumentValidator(ObjectValidator[DOC_SCH]):
    pass


DOC_VAL = TypeVar('DOC_VAL', bound=DocumentValidator)
