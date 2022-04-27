from dataclasses import dataclass
from os import PathLike
import os
from pathlib import Path
import typing as t

from lespy.confs.utils import python_file_for_dict


MIDDLEARE_ITEM_WITHOUT_ORDER = t.Iterable[t.Union[str, t.Callable]]
MIDDLEARE_ITEM_WITH_ORDER = t.Iterable[t.Union[str, t.Callable, int]]

MIDDLEARE_ITEM_ANY = t.Union[MIDDLEARE_ITEM_WITH_ORDER, MIDDLEARE_ITEM_WITHOUT_ORDER]

@dataclass
class MiddlewaresManager:
    request: t.List[MIDDLEARE_ITEM_ANY]
    response: t.List[MIDDLEARE_ITEM_ANY]
    
    def register_middleware(
        self,
        type: str,
        name: str,
        callable: t.Callable,
        order: t.Optional[int] = None
    ) -> None:
        _middleware = [name, callable]
        
        if order and isinstance(order, int):
            _middleware.append(order)
            
        if not (middlewares := getattr(self, type)):
            middlewares = [_middleware]
            return
        
        middlewares.append(_middleware)
        self._fn_middlewares_cache = []
    
    def register_request_middlewares(self, *middlewares: t.List[MIDDLEARE_ITEM_ANY]) -> None:
        for middleware in middlewares:
            self.register_middleware('request', *middleware)
    
    def register_response_middlewares(self, *middlewares: t.List[MIDDLEARE_ITEM_ANY]) -> None:
        for middleware in middlewares:
            self.register_middleware('response', *middleware)
    
    def get_middlewares(self, type: str) -> t.List[t.Callable]:
        try:
            if len(self._fn_middlewares_cache) > 0:
                return self._fn_middlewares_cache
        except:
            pass
        
        _with_order = []
        _without_order = []
        
        for mid in getattr(self, type, []):
            if len(mid) == 3:
                _with_order.append(mid)
                _with_order = [*sorted(_with_order, key=lambda m: m[2])]
                continue
            _without_order.append(mid)
        
        self._fn_middlewares_cache = [*map(lambda m: m[1], [*_with_order, *_without_order])]
        return self._fn_middlewares_cache
    
    def get_request_middlewares(self) -> t.List[t.Callable]:
        return self.get_middlewares('request')
    
    def get_response_middlewares(self) -> t.List[t.Callable]:
        return self.get_middlewares('response')


class ConfigsManager:
    def __init__(self, **initials) -> None:
        self.__dict__.update(initials)
        self.prefix = 'LESPY_'
    
    def get(self, key: str, default: t.Optional[t.Any] = None) -> t.Any:
        return getattr(self, key, default)
    
    def set(self, key: str, value: t.Any) -> None:
        self.__dict__[key] = value
    
    def has(self, key: str) -> bool:
        return hasattr(self, key)
    
    def load_from_env(self) -> None:
        envs = os.environ.items()
        
        for env, val in envs:
            if env.startswith(self.prefix):
                self.set(env.replace(self.prefix, ''), val)
    
    def load_from_mapping(self, mapping: t.Mapping) -> None:
        self.__dict__.update({**mapping})
    
    def load_from_py_file(self, path: t.Union[str, PathLike, Path]) -> None:
        self.load_from_mapping(python_file_for_dict(path))
