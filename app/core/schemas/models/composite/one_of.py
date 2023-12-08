from typing import Type

from pydantic import Field

from core.db.composite import OneOfComposite
from core.db.models import MODEL
from ._base import CompositeSchema, CompositeSchemaGenerator, composite_schemas
from .._schema_generator import kw_property
from ..._enums import CompositeTypes


__all__ = ["OneOfCompositeSchema", "OneOfCompositeSchemaGenerator"]


class OneOfCompositeSchema(CompositeSchema):
    nullable: bool
    original_cls: Type[OneOfComposite] = Field(exclude=True)


@composite_schemas.dispatch_for(type_=OneOfComposite)
class OneOfCompositeSchemaGenerator(CompositeSchemaGenerator[OneOfCompositeSchema, MODEL]):
    type = CompositeTypes.ONE_OF
    schema_cls = OneOfCompositeSchema

    @kw_property
    def original_cls(self):
        return self._comp.composite_class

    @kw_property
    def nullable(self) -> bool:
        return self._comp.composite_class.__nullable__
