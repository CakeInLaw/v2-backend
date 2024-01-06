from typing import Generic, Any, Type

from core.schema import A_SCH, COL_SCH, REL_SCH, Types
from ._base import CLAUSE, FilterOperand


__all__ = ["ClauseBuilder", "ColumnClauseBuilder", "RelationClauseBuilder"]


class ClauseBuilder(Generic[A_SCH]):

    @classmethod
    def build(cls, schema: A_SCH, op: FilterOperand, value: Any, full_path: str = None):
        full_path = full_path if full_path is not None else schema.name
        if schema.attr.is_column:
            builder = ColumnClauseBuilder
        elif schema.attr.is_relation:
            builder = RelationClauseBuilder
        else:
            raise ValueError(f'{schema} must be column or relation, not {schema}')
        return builder.build_clause(schema=schema, full_path=full_path, op=op, value=value)

    @classmethod
    def build_clause(cls, schema: A_SCH, full_path: str, op: FilterOperand, value: Any) -> CLAUSE:
        raise NotImplementedError


class ColumnClauseBuilder(ClauseBuilder[COL_SCH]):
    _reg: dict[tuple[Types, str], Type[CLAUSE]] = {}

    @classmethod
    def build_clause(cls, schema: A_SCH, full_path: str, op: FilterOperand, value: Any) -> CLAUSE:
        return cls._reg[(schema.type, op)](field=full_path, value=value)

    @classmethod
    def register(cls, t: Types, op: FilterOperand):
        def wrapper(filter_cls: Type[CLAUSE]) -> Type[CLAUSE]:
            cls._reg[(t, op)] = filter_cls
            return filter_cls
        return wrapper

    __new__ = object.__new__


class RelationClauseBuilder(ClauseBuilder[REL_SCH]):
    __new__ = object.__new__
