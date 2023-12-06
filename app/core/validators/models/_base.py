from typing import Generic, TypeVar

from core.schemas.models import M_SCH
from ..columns import get_column_validator, CV
from ..composites import get_composite_validator, CompV


__all__ = ["ModelValidator", "MV"]


class ModelValidator(Generic[M_SCH]):
    def __init__(self, schema: M_SCH):
        self._schema = schema

        self._columns: dict[str, CV] = {}
        for col_schema in self._schema.columns:
            self._columns[col_schema.name] = get_column_validator(col_schema)

        self._relations = {}

        self._composites: dict[str, CompV] = {}
        for comp_schema in self._schema.composites:
            self._composites[comp_schema.name] = get_composite_validator(comp_schema, self)

    def get_column(self, name: str) -> CV:
        return self._columns[name]

    def get_relation(self, name: str):
        return self._relations[name]

    def get_composite(self, name: str) -> CompV:
        return self._composites[name]


MV = TypeVar('MV', bound=ModelValidator)
