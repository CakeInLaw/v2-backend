from typing import Any, TYPE_CHECKING

from core.db.models import MODEL
from core.schemas import RelationTypes
from core.schemas.models.relations import ForwardRelationSchema
from ._base import RelationValidator
from ...exceptions import NotUnique

if TYPE_CHECKING:
    from core.repositories import O_REP
    from ..columns import COL_VAL

__all__ = ["ForwardRelationValidator"]


class ForwardRelationValidator(RelationValidator[ForwardRelationSchema, MODEL]):

    def _post_init(self):
        super()._post_init()
        self.local_attr_validator: "COL_VAL" = self.model_validator.get_column(self.schema.local_key)

    async def validate(self, value: MODEL, repository: "O_REP") -> None:
        if self.schema.type == RelationTypes.O2O:
            if not await repository.check_unique(attr_name=self.schema.name, value=value):
                raise NotUnique

    async def transform(self, value: Any, repository: "O_REP") -> MODEL:
        if isinstance(value, self._to_model):
            return value
        value = await self.local_attr_validator.transform(value=value, repository=repository)
        return await repository.get_related(rel_name=self.schema.name, pk=value)

    def modify_model_validator(self):
        if self.local_attr_validator.is_available():
            del self.model_validator.available_attrs[self.local_attr_validator.schema.name]
            self.model_validator.available_attrs[self.schema.name] = self
            if self.local_attr_validator.is_required():
                self.model_validator.required_attrs.remove(self.local_attr_validator.schema.name)
                self.model_validator.required_attrs.add(self.schema.name)
