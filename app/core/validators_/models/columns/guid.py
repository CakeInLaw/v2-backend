from uuid import UUID

from core.schemas.models.columns import GuidSchema
from ._base import ColumnValidator


__all__ = ["GuidValidator"]


class GuidValidator(ColumnValidator[GuidSchema, UUID]):
    python_type = UUID

    def _transform(self, value: str | UUID) -> UUID:
        if isinstance(value, str):
            value = UUID(value)
        return value
