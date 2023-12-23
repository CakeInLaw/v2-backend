from typing import TypeVar

from core.schemas.models import DocumentSchema
from ._object import ObjectValidator


__all__ = ["DocumentValidator", "DOC_VAL"]

DOC_VAL = TypeVar('DOC_VAL', bound="DocumentValidator")


class DocumentValidator(ObjectValidator[DocumentSchema]):
    pass
