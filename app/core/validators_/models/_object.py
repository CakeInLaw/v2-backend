from typing import TypeVar, Any

from core.schemas.models import O_SCH
from ._attrs import A_VAL
from ._base import ModelValidator
from ..exceptions import ObjectErrors, UnexpectedAttr, RequiredAttr, ValidationError


__all__ = ["ObjectValidator", "O_VAL"]

O_VAL = TypeVar('O_VAL', bound="ObjectValidator")


class ObjectValidator(ModelValidator[O_SCH]):

    async def transform_pk(self, value: Any):
        return await self.get_column(self.schema.primary_keys[0]).transform(value=value, repository=self.repository)

    async def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        create = self.repository.current_instance is None
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
        attr_validators: dict[str, A_VAL] = {}
        for attr, value in data.items():
            attr_validators[attr] = attr_validator = self.get_attr(attr)
            transformed_data[attr] = await attr_validator.transform(value=value, repository=self.repository)
        for attr, value in transformed_data.items():
            try:
                await attr_validators[attr].validate(value=value, repository=self.repository)
            except ValidationError as e:
                errors.add(attr, e)
        if errors:
            raise errors

        return transformed_data
