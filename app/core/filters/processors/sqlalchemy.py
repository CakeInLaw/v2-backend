from typing import Any

from sqlalchemy import ColumnElement, and_, or_, not_, Select
from sqlalchemy.orm import joinedload

from ._base import BaseFilterProcessor
from .. import groups, columns as cols, CLAUSE

__all__ = ["SaFilterProcessor"]


class SaFilterProcessor(BaseFilterProcessor[ColumnElement[bool]]):
    def apply_filters[S: Select](self, query: S, filters: dict[str, Any], **kwargs) -> S:
        return query.filter(*self.process_filters(filters, **kwargs))


@SaFilterProcessor.group(groups.AndClause)
def make_and_clause(clauses: list[ColumnElement[bool]], _) -> ColumnElement[bool]:
    assert clauses
    return and_(*clauses)


@SaFilterProcessor.group(groups.OrClause)
def make_or_clause(clauses: list[ColumnElement[bool]], _) -> ColumnElement[bool]:
    assert clauses
    return or_(*clauses)


@SaFilterProcessor.group(groups.NotClause)
def make_not_clause(clauses: list[ColumnElement[bool]], _) -> ColumnElement[bool]:
    assert clauses
    if len(clauses) == 1:
        return not_(clauses[0])
    else:
        return not_(and_(*clauses))


@SaFilterProcessor.clause(cols.BooleanEqualClause)
@SaFilterProcessor.clause(cols.DateEqualClause)
@SaFilterProcessor.clause(cols.DateTimeEqualClause)
@SaFilterProcessor.clause(cols.EnumEqualClause)
@SaFilterProcessor.clause(cols.GuidEqualClause)
@SaFilterProcessor.clause(cols.IntegerEqualClause)
@SaFilterProcessor.clause(cols.NumericEqualClause)
@SaFilterProcessor.clause(cols.StringEqualClause)
@SaFilterProcessor.clause(cols.TextEqualClause)
@SaFilterProcessor.clause(cols.TimeEqualClause)
def make_equal_clause(clause: CLAUSE, _):

