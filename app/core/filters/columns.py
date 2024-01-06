from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID

from core import types
from core.schema import Types
from ._base import BaseClause, FilterOperand as Op
from ._builders import ColumnClauseBuilder


__all__ = [
    "BooleanEqualClause", "BooleanNotEqualClause",

    "DateEqualClause", "DateNotEqualClause", "DateLtClause", "DateLteClause",
    "DateGtClause", "DateGteClause", "DateInClause", "DateNotInClause",

    "DateTimeEqualClause", "DateTimeNotEqualClause", "DateTimeLtClause", "DateTimeLteClause",
    "DateTimeGtClause", "DateTimeGteClause", "DateTimeInClause", "DateTimeNotInClause",

    "EnumEqualClause", "EnumNotEqualClause", "EnumInClause", "EnumNotInClause",

    "GuidEqualClause", "GuidNotEqualClause", "GuidInClause", "GuidNotInClause",

    "IntegerEqualClause", "IntegerNotEqualClause", "IntegerLtClause", "IntegerLteClause",
    "IntegerGtClause", "IntegerGteClause", "IntegerInClause", "IntegerNotInClause",

    "NumericEqualClause", "NumericNotEqualClause", "NumericLtClause", "NumericLteClause",
    "NumericGtClause", "NumericGteClause", "NumericInClause", "NumericNotInClause",

    "StringEqualClause", "StringNotEqualClause", "StringInClause", "StringNotInClause",
    "StringStartswithClause", "StringEndswithClause", "StringContainsClause",

    "TextEqualClause", "TextNotEqualClause", "TextInClause", "TextNotInClause",
    "TextStartswithClause", "TextEndswithClause", "TextContainsClause",

    "TimeEqualClause", "TimeNotEqualClause", "TimeLtClause", "TimeLteClause",
    "TimeGtClause", "TimeGteClause", "TimeInClause", "TimeNotInClause",
]


# Boolean ##############################################################################################################
@ColumnClauseBuilder.register(Types.BOOLEAN, Op.equal)
class BooleanEqualClause(BaseClause[bool]):
    pass


@ColumnClauseBuilder.register(Types.BOOLEAN, Op.not_equal)
class BooleanNotEqualClause(BaseClause[bool]):
    pass


# Date #################################################################################################################
@ColumnClauseBuilder.register(Types.DATE, Op.equal)
class DateEqualClause(BaseClause[date]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.not_equal)
class DateNotEqualClause(BaseClause[date]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.lt)
class DateLtClause(BaseClause[date]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.lte)
class DateLteClause(BaseClause[date]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.gt)
class DateGtClause(BaseClause[date]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.gte)
class DateGteClause(BaseClause[date]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.in_)
class DateInClause(BaseClause[list[date]]):
    pass


@ColumnClauseBuilder.register(Types.DATE, Op.not_in)
class DateNotInClause(BaseClause[list[date]]):
    pass


# DateTime #############################################################################################################
@ColumnClauseBuilder.register(Types.DATETIME, Op.equal)
class DateTimeEqualClause(BaseClause[datetime]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.not_equal)
class DateTimeNotEqualClause(BaseClause[datetime]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.lt)
class DateTimeLtClause(BaseClause[datetime]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.lte)
class DateTimeLteClause(BaseClause[datetime]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.gt)
class DateTimeGtClause(BaseClause[datetime]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.gte)
class DateTimeGteClause(BaseClause[datetime]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.in_)
class DateTimeInClause(BaseClause[list[datetime]]):
    pass


@ColumnClauseBuilder.register(Types.DATETIME, Op.not_in)
class DateTimeNotInClause(BaseClause[list[datetime]]):
    pass


# Enum #################################################################################################################
@ColumnClauseBuilder.register(Types.ENUM, Op.equal)
class EnumEqualClause(BaseClause[types.ENUM]):
    pass


@ColumnClauseBuilder.register(Types.ENUM, Op.not_equal)
class EnumNotEqualClause(BaseClause[types.ENUM]):
    pass


@ColumnClauseBuilder.register(Types.ENUM, Op.in_)
class EnumInClause(BaseClause[list[types.ENUM]]):
    pass


@ColumnClauseBuilder.register(Types.ENUM, Op.not_in)
class EnumNotInClause(BaseClause[list[types.ENUM]]):
    pass


# Guid #################################################################################################################
@ColumnClauseBuilder.register(Types.GUID, Op.equal)
class GuidEqualClause(BaseClause[UUID]):
    pass


@ColumnClauseBuilder.register(Types.GUID, Op.not_equal)
class GuidNotEqualClause(BaseClause[UUID]):
    pass


@ColumnClauseBuilder.register(Types.GUID, Op.in_)
class GuidInClause(BaseClause[list[UUID]]):
    pass


@ColumnClauseBuilder.register(Types.GUID, Op.not_in)
class GuidNotInClause(BaseClause[list[UUID]]):
    pass


# Integer ##############################################################################################################
@ColumnClauseBuilder.register(Types.INTEGER, Op.equal)
class IntegerEqualClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.not_equal)
class IntegerNotEqualClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.lt)
class IntegerLtClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.lte)
class IntegerLteClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.gt)
class IntegerGtClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.gte)
class IntegerGteClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.in_)
class IntegerInClause(BaseClause[int]):
    pass


@ColumnClauseBuilder.register(Types.INTEGER, Op.not_in)
class IntegerNotInClause(BaseClause[int]):
    pass


# Numeric ##############################################################################################################
@ColumnClauseBuilder.register(Types.NUMERIC, Op.equal)
class NumericEqualClause(BaseClause[Decimal]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.not_equal)
class NumericNotEqualClause(BaseClause[Decimal]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.lt)
class NumericLtClause(BaseClause[Decimal]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.lte)
class NumericLteClause(BaseClause[Decimal]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.gt)
class NumericGtClause(BaseClause[Decimal]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.gte)
class NumericGteClause(BaseClause[Decimal]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.in_)
class NumericInClause(BaseClause[list[Decimal]]):
    pass


@ColumnClauseBuilder.register(Types.NUMERIC, Op.not_in)
class NumericNotInClause(BaseClause[list[Decimal]]):
    pass


# String ###############################################################################################################
@ColumnClauseBuilder.register(Types.STRING, Op.equal)
class StringEqualClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.STRING, Op.not_equal)
class StringNotEqualClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.STRING, Op.in_)
class StringInClause(BaseClause[list[str]]):
    pass


@ColumnClauseBuilder.register(Types.STRING, Op.not_in)
class StringNotInClause(BaseClause[list[str]]):
    pass


@ColumnClauseBuilder.register(Types.STRING, Op.startswith)
class StringStartswithClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.STRING, Op.endswith)
class StringEndswithClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.STRING, Op.contains)
class StringContainsClause(BaseClause[str]):
    pass


# Text #################################################################################################################
@ColumnClauseBuilder.register(Types.TEXT, Op.equal)
class TextEqualClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.TEXT, Op.not_equal)
class TextNotEqualClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.TEXT, Op.in_)
class TextInClause(BaseClause[list[str]]):
    pass


@ColumnClauseBuilder.register(Types.TEXT, Op.not_in)
class TextNotInClause(BaseClause[list[str]]):
    pass


@ColumnClauseBuilder.register(Types.TEXT, Op.startswith)
class TextStartswithClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.TEXT, Op.endswith)
class TextEndswithClause(BaseClause[str]):
    pass


@ColumnClauseBuilder.register(Types.TEXT, Op.contains)
class TextContainsClause(BaseClause[str]):
    pass


# Time #################################################################################################################
@ColumnClauseBuilder.register(Types.TIME, Op.equal)
class TimeEqualClause(BaseClause[time]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.not_equal)
class TimeNotEqualClause(BaseClause[time]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.lt)
class TimeLtClause(BaseClause[time]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.lte)
class TimeLteClause(BaseClause[time]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.gt)
class TimeGtClause(BaseClause[time]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.gte)
class TimeGteClause(BaseClause[time]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.in_)
class TimeInClause(BaseClause[list[time]]):
    pass


@ColumnClauseBuilder.register(Types.TIME, Op.not_in)
class TimeNotInClause(BaseClause[list[time]]):
    pass
