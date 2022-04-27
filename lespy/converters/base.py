from typing import Any

class BaseConverter:
    regex: str
    convertor: Any = str
    
    def __init__(self, value: str):
        self._value = value
    
    @property
    def to_url(self) -> str:
        return str(self._value)
    
    @property
    def to_python(self) -> Any:
        return type(self).convertor(self._value)
