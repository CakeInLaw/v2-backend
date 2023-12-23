from core.db.models import DIRECTORY
from core.schemas.models import DirectorySchema
from core.validators_.models import DirectoryValidator
from ._object import ObjectRepository


class DirectoryRepository(ObjectRepository[DIRECTORY, DirectoryValidator, DirectorySchema]):
    _validator_cls = DirectoryValidator
