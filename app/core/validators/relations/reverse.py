from core.schemas.models.relations import ForwardRelationSchema
from ._base import RelationValidator


__all__ = ["ReverseRelationValidator"]


class ReverseRelationValidator(RelationValidator[ForwardRelationSchema]):
    pass

