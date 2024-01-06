from typing import TypeVar, Type, TYPE_CHECKING

from core.schema import ListSchema
from .models import ModelValidator

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

    def validate_list(self): ...  # TODO

    def validate_row(self): ...  # TODO


LIST_VAL = TypeVar('LIST_VAL', bound=ListValidator)
