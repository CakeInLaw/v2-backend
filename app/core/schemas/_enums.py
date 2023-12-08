import enum


__all__ = ["FieldTypes", "RelationTypes", "EnumSubTypes", "CompositeTypes"]


class FieldTypes(enum.StrEnum):
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
