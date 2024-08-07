from typing import Any

__all__ = [
    "ValidationError",
    "UnexpectedAttr",
    "RequiredAttr",
    "NonNullable",
    "NotUnique",
    "NotFound",
    "IncorrectFormat",
]


class ValidationError(Exception):
    def __init__(self, _code: str, **kwargs):
        self.code = _code
        self.kw = kwargs

    @property
    def params(self) -> dict[str, Any]:
        return self.kw

    def __call__(self, **kwargs):
        kw = {**self.kw, **kwargs} if self.kw else kwargs
        return self.__class__(self.code, **kw)

    def export(self):
        return {'code': self.code, **self.params}


UnexpectedAttr = ValidationError('unexpected_attr')
RequiredAttr = ValidationError('required_attr')
NonNullable = ValidationError('non_nullable')
NotUnique = ValidationError('non_unique')
NotFound = ValidationError('not_found')
IncorrectFormat = ValidationError('incorrect_format')
