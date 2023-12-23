from core.db.models import DOCUMENT
from core.schemas.models import DocumentSchema
from core.validators_.models import DocumentValidator
from ._object import ObjectRepository


class DocumentRepository(ObjectRepository[DOCUMENT, DocumentValidator, DocumentSchema]):
    _validator_cls = DocumentValidator

