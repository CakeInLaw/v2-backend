from typing import Any, TYPE_CHECKING

from core.schemas.models.relations import ForwardRelationSchema
from ._base import RelationValidator

if TYPE_CHECKING:
    from ..columns import CV

__all__ = ["ForwardRelationValidator"]


class ForwardRelationValidator(RelationValidator[ForwardRelationSchema]):

    async def validate(self, value: Any):
        pass

    async def transform(self, value: Any) -> Any:
        if isinstance(value, self._to_model):
            return value
        value = await self.local_attr.transform()

    @property
    def local_attr(self) -> "CV":

        return self._model_validator.get_column(self._schema.local_key)
