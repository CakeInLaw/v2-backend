from typing import TypeVar, Type

from sqlalchemy.orm import CompositeProperty

from core.db.models import MODEL
from core.db.composite import OneOfComposite
from core.schema.attrs import COMP_SCH, CompositeSchema, OneOfCompositeSchema
from ._base import AttrSchemaGenerator
from ._dispatcher import AttrSchemaGeneratorDispatcher
from ...gen_property import gen_property


__all__ = [
    "CompositeSchemaGenerator", "COMP_GEN",
    "CompositeSchemaGeneratorDispatcher", "composite_schema_generators",
    "OneOfCompositeSchemaGenerator"
]


class CompositeSchemaGenerator(AttrSchemaGenerator[COMP_SCH, CompositeProperty]):
    schema_cls = CompositeSchema

    @property
    def _comp(self):
        return self._attr

    @gen_property
    def name(self) -> str:
        return self._comp.key

    @gen_property
    def attrs(self) -> list[str]:
        return list(self._comp.attrs)


COMP_GEN = TypeVar('COMP_GEN', bound=CompositeSchemaGenerator)


class CompositeSchemaGeneratorDispatcher(AttrSchemaGeneratorDispatcher[COMP_GEN, type, CompositeProperty]):
    def _dispatch_by_attr(self, model: Type[MODEL], attr: CompositeProperty) -> Type[COMP_GEN]:
        for base in attr.composite_class.__mro__:
            if base in self._reg_map:
                return self._reg_map[base]
        raise ValueError(f'No {model} or it`s parent registered')


composite_schema_generators = CompositeSchemaGeneratorDispatcher()


@composite_schema_generators.dispatch_for(OneOfComposite)
class OneOfCompositeSchemaGenerator(CompositeSchemaGenerator[OneOfCompositeSchema]):
    schema_cls = OneOfCompositeSchema

    @gen_property
    def nullable(self) -> bool:
        return self._comp.composite_class.__nullable__
