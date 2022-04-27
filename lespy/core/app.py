import typing as t
from lespy.core.base import Base
from lespy.core.router import Route, Router, _C


class App(Base):
    def __init__(
        self,
        app_name: str,
        base_path: str = '/'
    ):
        self._app_name = app_name
        self._base_path = base_path

        self._router: Router = Router(self._base_path)

    def route(self, path: str, methods: t.List[str], route_name: t.Optional[str] = None) -> t.Callable[[_C], _C]:
        def inner(callback: _C) -> _C:
            nonlocal route_name, path, methods
            if not route_name:
                if '<lambda>' in (route_name := callback.__name__):
                    raise ValueError('A lambda function cannot be used when the route_name parameter is not set')
                
            route = Route(path, route_name, methods, callback)
            self._router.add_route(route)
            return callback
        return inner

    def get(self, path: str, route_name: t.Optional[str] = None) -> t.Callable[[_C], _C]:
        return self.route(path, ['GET'], route_name)

    def post(self, path: str, route_name: t.Optional[str] = None) -> t.Callable[[_C], _C]:
        return self.route(path, ['POST'], route_name)

    def _find_rule(self, path: str, method: str) -> t.Tuple[Route, t.Dict[str, t.Any]]:
        return self._router.match(path, method)

    def url_for(self, name: str, **params) -> str:
        route: Route = self._router.find_by_name(name.strip())
        return route.reverse(**params)
