import enum
from typing import TypeVar, Union


__all__ = ["BaseClause", "CLAUSE", "BaseClauseGroup", "CLAUSE_GROUP", "FilterOperand", "ClauseGroupType"]


class BaseClause[T]:
    is_group = False

    def __init__(self, field: str, value: T):
        self.field = field
        self.value = value


class BaseClauseGroup:
    is_group = True

    def __init__(self, clauses: list[Union["CLAUSE", "CLAUSE_GROUP"]]):
        self.clauses = clauses


CLAUSE = TypeVar('CLAUSE', bound=BaseClause)
CLAUSE_GROUP = TypeVar('CLAUSE_GROUP', bound=BaseClauseGroup)


class FilterOperand(enum.StrEnum):
    equal = '=='
    not_equal = '!='
    lt = '<'
    lte = '<='
    gt = '>'
    gte = '>='
    in_ = 'in'
    not_in = 'not_in'

    # String and Text only
    startswith = 'startswith'
    endswith = 'endswith'
    contains = 'contains'


class ClauseGroupType(enum.StrEnum):
    AND = '[and]'
    OR = '[or]'
    NOT = '[not]'
