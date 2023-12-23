from typing import Any, TypeVar

from core.schemas.models import ListModelSchema
from ._base import ModelValidator


__all__ = ["ListModelValidator", "LIST_VAL"]

LIST_VAL = TypeVar('LIST_VAL', bound="ListModelValidator")


class ListModelValidator(ModelValidator[ListModelSchema]):
    async def validate_row(self, data: dict[str, Any]):
        pass

    async def validate_list(self, data: list[dict[str, Any]]):
        pass

    async def transform_row(self, data: dict[str, Any]):
        pass

    async def transform_list(self, data: list[dict[str, Any]]):
        pass
