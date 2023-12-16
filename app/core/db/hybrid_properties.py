from typing import TypeVar

from sqlalchemy.ext.hybrid import hybrid_property, _HybridGetterType

T = TypeVar('T')


def hybrid_property_helper(
        required: bool = False,
        readable: bool = True,
        writeable: bool = True,
        **kwargs
):
    def wrapper(func: _HybridGetterType[T]) -> hybrid_property[T]:
        prop = hybrid_property(func)
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
