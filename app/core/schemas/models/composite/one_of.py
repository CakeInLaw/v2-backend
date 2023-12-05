from typing import TypeVar

from core.db.composite import OneOfComposite
from core.db.models import MODEL
from ._base import CompositeSchema, CompositeSchemaGenerator, composite_schemas
from ..._enums import CompositeTypes


__all__ = ["OneOfCompositeSchema", "OneOfCompositeSchemaGenerator"]
OOC_SCH = TypeVar("OOC_SCH", bound="OneOfCompositeSchema")


class OneOfCompositeSchema(CompositeSchema):
    pass


@composite_schemas.dispatch_for(type_=OneOfComposite)
class OneOfCompositeSchemaGenerator(CompositeSchemaGenerator[OOC_SCH, MODEL]):
    type = CompositeTypes.ONE_OF
    schema_cls = OneOfCompositeSchema
