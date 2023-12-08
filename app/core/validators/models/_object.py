from typing import TypeVar, Any, TYPE_CHECKING

from core.schemas.models import O_SCH
from ._base import ModelValidator
from ..exceptions import ObjectErrors, UnexpectedAttr, RequiredAttr, ValidationError

if TYPE_CHECKING:
    from core.repositories import O_REP


__all__ = ["ObjectValidator", "O_VAL"]


class ObjectValidator(ModelValidator[O_SCH]):
    async def validate(self, data: dict[str, Any], repository: "ORepo") -> dict[str, Any]:
        create = repository.current_instance is None
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

        transformed_data = {}
        for attr, value in data.items():
            if attr in self._columns:
                attr_validator = self.get_attr(attr)
                value = await attr_validator.transform(value)
                try:
                    await attr_validator.validate(value)
                    transformed_data[attr] = value
                except ValidationError as e:
                    errors.add(attr, e)
        if errors:
            raise errors

        return transformed_data


O_VAL = TypeVar('O_VAL', bound=ObjectValidator)
