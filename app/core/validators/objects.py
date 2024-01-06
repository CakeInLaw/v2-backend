from typing import Any, TYPE_CHECKING, Type, TypeVar

from core.schema import O_SCH, DIR_SCH, DOC_SCH
from .models import ModelValidator
from .lists import ListValidator
from .exceptions import ObjectErrors, UnexpectedAttr, RequiredAttr

if TYPE_CHECKING:
    from core.repositories import O_REP


__all__ = [
    "ObjectValidator", "O_VAL",
    "DirectoryValidator", "DIR_VAL",
    "DocumentValidator", "DOC_VAL",
]


class ObjectValidator(ModelValidator[O_SCH]):
    _lists: dict[str, Type[ListValidator]]

    def __init__(self, repository: "O_REP"):
        self.repository = repository

    @classmethod
    def bind(cls: Type["O_VAL"], schema: O_SCH) -> Type["O_VAL"]:
        return type(f'{schema.name}{cls.__name__}', (cls, ), {}, schema=schema)  # type: ignore

    def get_list(self, name: str) -> ListValidator:
        return self._lists[name](repository=self.repository.list_repository(name))

    async def validate(self, data: dict[str, Any]) -> dict[str, Any]:  # TODO
        create = self.repository.instance is not None
        errors = ObjectErrors()

        for attr in data:
            if attr not in self.available_attrs:
                errors.add(attr, UnexpectedAttr)
        if create:
            for attr in self.required_attrs:
                if attr not in data:
                    errors.add(attr, RequiredAttr)
        if errors:
            raise errors

        valid_data = {}

    def __init_subclass__(cls, schema: O_SCH = None):
        super().__init_subclass__(schema=schema)
        if schema is None:
            return

        cls._lists = {
            list_schema.name: ListValidator.bind(schema=list_schema)
            for list_schema in cls.schema.get_lists()
        }


O_VAL = TypeVar('O_VAL', bound=ObjectValidator)


class DirectoryValidator(ObjectValidator[DIR_SCH]):
    pass


DIR_VAL = TypeVar('DIR_VAL', bound=DirectoryValidator)


class DocumentValidator(ObjectValidator[DOC_SCH]):
    pass


DOC_VAL = TypeVar('DOC_VAL', bound=DocumentValidator)
