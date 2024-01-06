import enum


__all__ = ["Attrs", "Types", "Relations", "EnumSubTypes", "Composites"]


class Attrs(enum.StrEnum):
    COLUMN = 'column'
    PROPERTY = 'property'
    RELATION = 'relation'
    COMPOSITE = 'composite'
    LIST = 'list'

    @property
    def is_column(self) -> bool:
        return self is Attrs.COLUMN

    @property
    def is_property(self) -> bool:
        return self is Attrs.PROPERTY

    @property
    def is_relation(self) -> bool:
        return self is Attrs.RELATION

    @property
    def is_composite(self) -> bool:
        return self is Attrs.COMPOSITE

    @property
    def is_list(self) -> bool:
        return self is Attrs.LIST


class Types(enum.StrEnum):
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


class Relations(enum.StrEnum):
    O2O = 'o2o'
    REV_O2O = 'reverse_o2o'
    FK = 'fk'
    REV_FK = 'reverse_fk'

    @classmethod
    def forward(cls):
        return cls.O2O, cls.FK

    @property
    def is_forward(self) -> bool:
        return self in self.forward()

    @classmethod
    def reverse(cls):
        return cls.REV_O2O, cls.REV_FK

    @property
    def is_reverse(self) -> bool:
        return self in self.reverse()


class Composites(enum.StrEnum):
    ONE_OF = 'one_of'


class EnumSubTypes(enum.StrEnum):
    STRING = 'string'
    INTEGER = 'integer'
