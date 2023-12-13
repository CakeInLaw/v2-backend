from core.db.models import OBJECT
from core.schemas.models.relations import ForwardRelationSchema
from ._base import RelationValidator


__all__ = ["ReverseRelationValidator"]


class ReverseRelationValidator(RelationValidator[ForwardRelationSchema, OBJECT]):
    pass
