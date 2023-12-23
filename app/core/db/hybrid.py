from typing import TypeVar, Any

from sqlalchemy.ext.hybrid import hybrid_property

_T = TypeVar('_T', bound=Any)


def hybrid_property_helper(
        required: bool = False,
        readable: bool = True,
        writeable: bool = True,
        **kwargs
):
    """
    Usage example
    @hybrid_property_helper(
        required=True,
        setter_pattern='^(?=.*[A-Za-z])(?=.*[0-9])[A-Za-z0-9!@#$%^&*-_=+]{8,30}$',
        setter_min_length=8,
        setter_max_length=30,
    )
    @hybrid_property
    def password(self) -> str:
        return getattr(self, '_orig_password', None)

    """

    def wrapper(prop: hybrid_property[_T]) -> hybrid_property[_T]:
        prop.info.update({
            'required': required,
            'readable': readable,
            'writeable': writeable,
            'getter': (getter_params := {}),
            'setter': (setter_params := {}),
        })
        for k, v in kwargs.items():
            if k.startswith('_'):
                getter_params[k.lstrip('_')] = v
                setter_params[k.lstrip('_')] = v
            elif k.startswith('getter_'):
                getter_params[k.lstrip('getter_')] = v
            elif k.startswith('setter_'):
                setter_params[k.lstrip('setter_')] = v
            else:
                raise Exception(f'{k} is unexpected kwarg')
        return prop
    return wrapper
