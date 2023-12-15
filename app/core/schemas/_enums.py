import enum


__all__ = ["AttrTypes", "ColumnTypes", "RelationTypes", "EnumSubTypes", "CompositeTypes"]


class AttrTypes(enum.StrEnum):
    COLUMN = 'column'
    RELATION = 'relation'
    COMPOSITE = 'composite'
    PROPERTY = 'property'


class ColumnTypes(enum.StrEnum):
    BOOLEAN = 'boolean'
    DATE = 'date'
    DATETIME = 'datetime'
    ENUM = 'enum'
    GUID = 'guid'
    INTEGER = 'integer'
    NUMERIC = 'numeric'
    STRING = 'string'
    TEXT = 'text'
    TIME = 'time'


class RelationTypes(enum.StrEnum):
    O2O = 'o2o'
    REV_O2O = 'reverse_o2o'
    FK = 'fk'
    REV_FK = 'reverse_fk'


class EnumSubTypes(enum.StrEnum):
    STRING = 'string'
    INTEGER = 'integer'


class CompositeTypes(enum.StrEnum):
    ONE_OF = 'one_of'
