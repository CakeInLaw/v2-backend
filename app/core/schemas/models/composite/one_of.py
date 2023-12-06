from typing import TypeVar

from core.db.composite import OneOfComposite
from core.db.models import MODEL
from ._base import CompositeSchema, CompositeSchemaGenerator, composite_schemas
from ..._enums import CompositeTypes


__all__ = ["OneOfCompositeSchema", "OneOfCompositeSchemaGenerator"]


class OneOfCompositeSchema(CompositeSchema):
    pass


@composite_schemas.dispatch_for(type_=OneOfComposite)
class OneOfCompositeSchemaGenerator(CompositeSchemaGenerator[OneOfCompositeSchema, MODEL]):
    type = CompositeTypes.ONE_OF
    schema_cls = OneOfCompositeSchema
