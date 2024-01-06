from typing import Any, TYPE_CHECKING

from core.constants import EMPTY
from core.schema import REL_SCH, FWD_REL_SCH, REV_REL_SCH
from ._base import AttrValidator, ParentRepository, AttrValidatorParent
from ..exceptions import NotFound, ListErrors

if TYPE_CHECKING:
    from core.repositories import LIST_REP


__all__ = ["RelationValidator", "ForwardRelationValidator", "ReverseRelationValidator", "get_relation_validator"]

NotFoundRelValue = object()


class RelationValidator(AttrValidator[REL_SCH, Any]):
    pass


class ForwardRelationValidator(RelationValidator[FWD_REL_SCH]):
    def _post_init(self):
        self.local_attr = self.parent.get_column(self.schema.local_key)

    async def validate(self, value: Any, repository: ParentRepository):
        value = self.local_attr.validate(value=value, repository=repository)
        if value is None:
            return
        value = await repository.related_repository(self.schema.name).get_one(value)
        if value is None:
            raise NotFound
        return value

    async def validate_list(self, list_of_values: list[Any], repository: LIST_REP) -> list[Any]:
        valid_identifiers = self.local_attr.validate_list(list_of_values, repository=repository)
        rel_objects: dict = await repository.related_repository(self.schema.name).get_many(
            list(filter(lambda i: i is not EMPTY, valid_identifiers))
        )
        validated = []
        list_errors = ListErrors()
        for idx, valid_id in enumerate(valid_identifiers):
            if valid_id is EMPTY:
                validated.append(valid_id)
            elif valid_id in rel_objects:
                validated.append(rel_objects[valid_id])
            else:
                list_errors.add(idx, err=NotFound)
        if list_errors:
            raise list_errors
        return validated

    def modify_parent(self):
        if self.schema.local_key in self.parent.available_attrs:
            del self.parent.available_attrs[self.schema.local_key]
            self.parent.available_attrs[self.schema.name] = self
            if self.schema.local_key in self.parent.required_attrs:
                self.parent.required_attrs.remove(self.schema.local_key)
                self.parent.required_attrs.add(self.schema.name)


class ReverseRelationValidator(RelationValidator[REV_REL_SCH]):
    pass


def get_relation_validator(schema: REL_SCH, parent: AttrValidatorParent) -> RelationValidator:
    if schema.type.is_forward:
        return ForwardRelationValidator(schema=schema, parent=parent)
    else:
        return ReverseRelationValidator(schema=schema, parent=parent)
