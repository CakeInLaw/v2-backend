from typing import Type, Any, Sequence, Protocol

from core.schema import O_SCH, AppSchema, get_default_app_schema, REL_SCH
from .._base import CLAUSE, CLAUSE_GROUP, FilterOperand, ClauseGroupType
from .._builders import ClauseBuilder
from ..groups import AndClause, OrClause, NotClause


__all__ = ["BaseFilterProcessor"]


class ClauseProcessor[_T](Protocol):
    def __call__(self, clause: CLAUSE, others: dict[str, Any]) -> _T: ...


class ClauseGroupProcessor[_T](Protocol):
    def __call__(self, clauses: list[_T], others: dict[str, Any]) -> _T: ...


class BaseFilterProcessor[_T]:
    _clause_processor: dict[Type[CLAUSE], ClauseProcessor[_T]]
    _group_processor: dict[Type[CLAUSE_GROUP], ClauseGroupProcessor[_T]]

    def __init__(self, schema: O_SCH, app_schema: AppSchema = None):
        self.schema = schema
        self.app_schema = app_schema if app_schema is not None else get_default_app_schema()

    def __init_subclass__(cls):
        cls._clause_processor = {}
        cls._group_processor = {}

    @classmethod
    def clause(cls, clause: Type[CLAUSE]):
        def register_executor(func: ClauseProcessor[_T]):
            cls._clause_processor[clause] = func
            return func
        return register_executor

    @classmethod
    def group(cls, group: Type[CLAUSE_GROUP]):
        def register_group(func: ClauseGroupProcessor[_T]):
            cls._group_processor[group] = func
            return func
        return register_group

    def build_clauses(self, filters: dict[str, Any]) -> list[CLAUSE | CLAUSE_GROUP]:
        clauses = []
        for key, value in filters.items():
            if key.startswith('['):
                assert isinstance(value, dict), f'Value is not a dict: {value}'
                group_type = ClauseGroupType(key)
                if group_type is ClauseGroupType.AND:
                    clauses.append(AndClause(*self.build_clauses(value)))
                elif group_type is ClauseGroupType.OR:
                    clauses.append(OrClause(*self.build_clauses(value)))
                elif group_type is ClauseGroupType.NOT:
                    clauses.append(NotClause(*self.build_clauses(value)))
                else:
                    raise RuntimeError(f"Unknown group type {group_type}")
            else:
                clauses.append(self.build_clause(key, *self.get_operand_and_value(value)))
        return clauses

    def build_clause(self, key: str, op: FilterOperand, value: Any) -> CLAUSE:
        schema = self.schema
        if '.' in key:
            *rel_names, col_name = key.split('.')
            for rel_name in rel_names:
                rel: REL_SCH = schema.get_attr(rel_name)
                assert rel.attr.is_relation
                schema = self.app_schema.get_reference(rel.to_model)
        return ClauseBuilder.build(schema=schema.get_attr(key), op=op, value=value, full_path=key)

    @classmethod
    def get_operand_and_value(cls, value: Sequence[str, Any]) -> tuple[FilterOperand, Any]:
        assert isinstance(value, Sequence) and len(value) == 2, 'value must be like [operand, value]'
        op, filter_value = value
        return FilterOperand(op), filter_value

    def process_filters(self, filters: dict[str, Any], **kwargs) -> list[_T]:
        others = {**kwargs, 'schema': self.schema, 'app_schema': self.app_schema}
        return self.process_clauses(self.build_clauses(filters), others=others)

    def process_clauses(self, clauses: list[CLAUSE | CLAUSE_GROUP], others: dict[str, Any]) -> list[_T]:
        processed_clauses = []
        for clause in clauses:
            if clause.is_group:
                processed_clauses.append(self.process_clause_group(clause, others=others))
            else:
                processed_clauses.append(self.process_clause(clause, others=others))
        return processed_clauses

    def process_clause(self, clause: CLAUSE, others: dict[str, Any]) -> _T:
        return self._clause_processor[clause.__class__](clause, others)

    def process_clause_group(self, clause_group: CLAUSE_GROUP, others: dict[str, Any]) -> _T:
        processed_clauses = self.process_clauses(clause_group.clauses, others=others)
        return self._group_processor[clause_group.__class__](processed_clauses, others)
