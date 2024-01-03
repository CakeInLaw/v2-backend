from typing import Any

from core.schema import PROP_SCH
from ._base import AttrValidator, ParentRepository, AttrValidatorParent
from ._constraints import get_constraints_validator
from ..exceptions import IncorrectFormat

__all__ = ["PropertyValidator", "get_property_validator"]


class PropertyValidator(AttrValidator[PROP_SCH, Any]):
    def _post_init(self):
        if self.schema.setter_type is None:
            return
        self._constr_validator = get_constraints_validator(self.schema.setter_constraints)
        for validator in self._constr_validator.get_validators():
            self.add_validator(validator)

    async def validate(self, value: Any, repository: ParentRepository) -> Any:
        try:
            value = self._constr_validator.transform(value=value)
        except Exception as e:
            raise IncorrectFormat(detail=str(e))
        if value is None:
            self.raise_if_non_nullable()
            return
        for validator in self._validators:
            await validator(value=value, repository=repository)

    def modify_parent(self):
        if self.schema.setter_type is not None:
            self.parent.available_attrs[self.schema.name] = self
            if self.schema.required:
                self.parent.required_attrs.add(self.schema.name)


def get_property_validator(schema: PROP_SCH, parent: AttrValidatorParent) -> PropertyValidator:
    return PropertyValidator(schema=schema, parent=parent)
