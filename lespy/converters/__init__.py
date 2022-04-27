import typing as t

from functools import lru_cache
from lespy.converters.base import BaseConverter
import lespy.converters.converters as lespy_converters
from lespy.utils import to_snake_case

CONVERTERS = {
    'int': lespy_converters.IntConverter,
    'str': lespy_converters.StringConverter,
    'slug': lespy_converters.SlugConverter,
    'uuid': lespy_converters.UUIDConverter,
    'path': lespy_converters.PathConverter,
}

@lru_cache(None)
def get_converter(key: str):
    return CONVERTERS.get(key)

def register_converter(key: t.Optional[t.Union[str, t.Callable]] = None, converter: t.Optional[t.Callable] = None):

    if key is not None and converter is None:
        # @register_converter
        # class DateConverter(BaseConverter):
        if callable(key):
            converter, key = key, key.__name__
            key = to_snake_case(key).replace('_converter', '')
            register_converter(key, converter)
            return converter
        
        # @register_converter('date')
        # class DateConverter(BaseConverter):
        def inner(converter: t.Callable):
            register_converter(key, converter)
            return converter
        return inner

    # register_converter('date', DateConverter)
    elif isinstance(key, str) and callable(converter):
        CONVERTERS[key] = converter
        get_converter.cache_clear()
        return

    raise ValueError("'key' must be of type str and 'converter' must be a class-style callable object.")   

__all__ = [
    'BaseConverter',
    'get_converter',
    'register_converter',
]
