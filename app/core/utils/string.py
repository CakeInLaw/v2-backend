import re


__all__ = ["camel_to_snake"]

camel_to_snake_reg = re.compile(r'(?!^)(?<!_)([A-Z])')


def camel_to_snake(s):
    return camel_to_snake_reg.sub(r'_\1', s).lower()
