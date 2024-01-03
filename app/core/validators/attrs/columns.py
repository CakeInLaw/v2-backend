from typing import TypeVar, Type, Any, final, Generic

from core.schema import COL_SCH
from ._base import AttrValidator, ParentRepository, AttrValidatorParent
from ._constraints import CONSTR_VAL, get_constraints_validator
from ..exceptions import NotUnique, IncorrectFormat

__all__ = ["ColumnValidator", "get_column_validator"]


T = TypeVar('T', bound=Any)


class ColumnValidator(AttrValidator[COL_SCH, T], Generic[COL_SCH, T, CONSTR_VAL]):
    _constr_validator_cls: Type[CONSTR_VAL]

    def _post_init(self):
        self._constr_validator = get_constraints_validator(constraint=self.schema.constraints)
        for validator in self._constr_validator.get_validators():
            self.add_validator(validator)
        if self.should_validate_unique():
            self.add_validator(self._validate_unique)

    @final
    async def validate(self, value: Any, repository: ParentRepository) -> T:
        try:
            value = self._constr_validator.transform(value=value)
        except Exception as e:
            raise IncorrectFormat(detail=str(e))
        if value is None:
            self.raise_if_non_nullable()
            return
        for validator in self._validators:
            await validator(value=value, repository=repository)

    def is_available(self) -> bool:
        return not (self.schema.hidden or self.schema.read_only)

    def is_required(self) -> bool:
        return not self.schema.has_default

    def modify_parent(self):
        if self.is_available():
            self.parent.available_attrs[self.schema.name] = self
            if self.is_required():
                self.parent.required_attrs.add(self.schema.name)

    def should_validate_unique(self):
        if self.parent.is_list:
            return False
        pks = self.parent.schema.primary_keys
        return self.schema.unique or (len(pks) == 1 and pks[0] == self.schema.name)

    async def _validate_unique(self, value: Any, repository: ParentRepository):
        if not await repository.is_unique(self.schema.name, value=value):
            raise NotUnique


def get_column_validator(schema: COL_SCH, parent: AttrValidatorParent) -> ColumnValidator:
    return ColumnValidator(schema=schema, parent=parent)
