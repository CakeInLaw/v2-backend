from typing import Any, TypeVar, Sequence, TYPE_CHECKING

from core.constants import EMPTY
from core.schema import COMP_SCH, OneOfCompositeSchema, Composites
from ._base import AttrValidator, A_VAL, ParentRepository, AttrValidatorParent
from ..exceptions import ValidationError, IncorrectFormat, IncorrectAttr, ListErrors, NonNullable

if TYPE_CHECKING:
    from core.repositories import LIST_REP

__all__ = ["CompositeValidator", "OneOfCompositeValidator", "get_composite_validator"]

T = TypeVar('T', bound=Any)


class CompositeValidator(AttrValidator[COMP_SCH, T]):
    pass


class OneOfCompositeValidator(CompositeValidator[OneOfCompositeSchema, tuple[str, Any]]):
    def _post_init(self):
        for attr in self.schema.attrs:
            setattr(self, f'_attr_cached_{attr}', self.parent.get_attr(attr))

    def get_attr(self, attr: str) -> A_VAL:
        return getattr(self, f'attr_cached_{attr}')

    async def validate(self, value: Any, repository: ParentRepository) -> tuple[str, Any] | None:
        if value is None:
            self.raise_if_non_nullable()
            return
        if not isinstance(value, Sequence) and not len(value) == 2:
            raise IncorrectFormat(f'"(col_name, col_value)" expected, got {value}')
        attr_name, value = value
        if attr_name not in self.schema.attrs:
            raise IncorrectAttr(attr_name)
        try:
            return attr_name, await self.get_attr(attr_name).validate(value=value, repository=repository)
        except ValidationError as e:
            raise e(attr=attr_name)

    async def validate_list(self, list_of_values: list, repository: LIST_REP) -> None:
        real_attr_ids = {attr: [] for attr in self.schema.attrs}
        valid_values_lists = {}
        list_errors = ListErrors()
        for idx, value in enumerate(list_of_values):
            if value is EMPTY:
                valid_values_lists[idx] = EMPTY
                continue
            elif value is None:
                if self.is_nullable:
                    valid_values_lists[idx] = None
                else:
                    list_errors.add(idx, err=NonNullable)
            else:
                if not isinstance(value, Sequence) and not len(value) == 2:
                    list_errors.add(idx, IncorrectFormat(f'"(col_name, col_value)" expected, got {value}'))
                    continue
                attr_name, value = value
                if attr_name in self.schema.attrs:
                    real_attr_ids[attr_name].append(idx)
                else:
                    list_errors.add(idx, err=IncorrectAttr(attr_name))
        if list_errors:
            raise list_errors
        for attr_name in self.schema.attrs:
            ids = real_attr_ids[attr_name]
            if not ids:
                continue
            try:
                valid_attr_list_of_values = await self.get_attr(attr_name).validate_list(
                    [list_of_values[i] for i in ids], repository=repository
                )
                for idx, value in enumerate(valid_attr_list_of_values):
                    valid_values_lists[ids[idx]] = value
            except ListErrors as error:
                for idx, err in error:
                    list_errors.add(ids[idx], err=err)
        if list_errors:
            raise list_errors
        return valid_values_lists

    def modify_parent(self):
        for attr in self.schema.attrs:
            assert attr in self.parent.available_attrs, \
                f'{self.schema.owner}.{attr} is not available. Cannot apply one of composite'
            assert attr not in self.parent.required_attrs, \
                f'{self.schema.owner}.{attr} is required. Cannot apply one of composite'
            del self.parent.available_attrs[attr]
        self.parent.available_attrs[self.schema.name] = self


composite_validators_map = {
    Composites.ONE_OF: OneOfCompositeValidator,
}


def get_composite_validator(schema: COMP_SCH, parent: AttrValidatorParent) -> CompositeValidator:
    return composite_validators_map[schema.type](schema=schema, parent=parent)
