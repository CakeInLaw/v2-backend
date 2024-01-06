from typing import TypeVar, Type, TYPE_CHECKING, Any

from core.schema import ListSchema
from .exceptions import ObjectErrors, ListErrors, UnexpectedAttr, RequiredAttr
from .models import ModelValidator
from ..constants import EMPTY

if TYPE_CHECKING:
    from core.repositories import LIST_REP

__all__ = ["ListValidator", "LIST_VAL"]


class ListValidator(ModelValidator[ListSchema]):
    is_list: bool = True

    def __init__(self, repository: "LIST_REP"):
        self.repository = repository

    @classmethod
    def bind(cls: Type["LIST_VAL"], schema: ListSchema) -> Type["LIST_VAL"]:
        return type(f'{schema.name}{cls.__name__}', (cls, ), {}, schema=schema)  # type: ignore

    async def validate_list(self, list_data: list[dict[str, Any]]):
        list_errors = ListErrors()
        all_attrs = set()
        for idx, data in enumerate(list_data):
            errors = ObjectErrors()
            for attr in data:
                all_attrs.add(attr)
                if attr not in self.available_attrs:
                    errors.add(attr, UnexpectedAttr)
            for attr in self.required_attrs:
                if attr not in data:
                    errors.add(attr, RequiredAttr)
            if errors:
                list_errors.add(idx, err=errors)
        if list_errors:
            raise list_errors

        valid_data = tuple(dict() for _ in range(len(list_data)))
        for attr in all_attrs:
            try:
                valid_list_of_values = await self.get_available_attr(attr).validate_list(
                    [data.get(attr, EMPTY) for data in list_data], repository=self.repository
                )
                for i, value in enumerate(valid_list_of_values):
                    if value is not EMPTY:
                        valid_data[i][attr] = value
            except ListErrors as errors:
                for idx, err in errors:
                    list_errors.add(idx, err=err)
        if list_errors:
            raise list_errors
        return valid_data

    async def validate_row(self, data: dict[str, Any]): ...  # TODO


LIST_VAL = TypeVar('LIST_VAL', bound=ListValidator)
