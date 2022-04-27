import re
import typing as t
from lespy.http.request import Request
from lespy.http.response import ResponseBase
from lespy.http.utils import make_url
from lespy.exceptions import RouteAlreadyExists, RouteNotFound
from lespy.converters import get_converter, BaseConverter


_C = t.Callable[[Request], t.Union[ResponseBase, str, dict, int, list]]

# E.g. /<name>/ or /<str:name>/
_REGEX_PATH = re.compile(r'<(?:(?P<converter>[^>:]+):)?(?P<parameter>[^>]+)>')

def compile_route(route: str) -> t.Tuple[str, t.Dict[str, BaseConverter]]:
    """Compile a route to regex

    Args:
        route (str): route to compile

    Returns:
        t.Tuple[str, t.Dict[str, BaseConverter]]: regex the route and dict with param name and your converter
    
    Examples:
        >>> compile_route('/user/<id:int>')
        ('^/user/(?P<id>[0-9]+)/$', {'id': <class 'lespy.converters.converters.IntConverter'>})
        >>> compile_route('/')
        ('^/$', {})
    """
    parts = ['^']
    converters = {}
    
    while True:
        match = _REGEX_PATH.search(route)
        
        if not match:
            parts.append(re.escape(route))
            break
        
        parts.append(re.escape(route[:match.start()]))
        route = route[match.end():]
        
        parameter = match['parameter']
        converter = get_converter(match['converter'] or 'str')
        converters[parameter] = converter
        parts.append(f'(?P<{parameter}>{converter.regex})')
        
    return ''.join([*parts, '$']), converters


class Route:
    _path: str
    _re_path: str
    _converters: t.Dict[str, BaseConverter]
    def __init__(
        self,
        path: str,
        route_name: str,
        methods: t.List[str],
        callback: _C
    ):
        """Make a route object

        Args:
            path (str): Path for this route e.g. '/' or '/user/<int:int>'
            route_name (str): route name e.g. 'home'
            methods (t.List[str]): A list of methods for this route
            callback (t.Callable[[Request], ResponseBase]): Function to be executed when the route is called
        
        Examples:
            >>> route = Route('/user/<int:id>/', 'get_user', ['GET'], get_user_function)
        """
        self.path = path
        self.name = route_name
        self.methods = [*map(lambda method: method.upper(), methods)]
        self.callback = callback

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str):
        assert not path is None, 'The path cannot None'
        
        self._path = make_url(None, '/', path)
        self._re_path, self.converters = compile_route(self._path)

    @property
    def converters(self) -> t.Dict[str, BaseConverter]:
        return self._converters

    @converters.setter
    def converters(self, convs: t.Dict[str, BaseConverter]):
        self._converters = convs

    def reverse(self, **params: t.Dict[str, t.Any]) -> str:
        """Reverse the route

        Returns:
            str: url path mounted with the params
        
        Examples:
            >>> route.reverse(id=100)
            '/user/100/'
        """
        def repl(match: t.Match[t.AnyStr]) -> str:
            param = match.group('param')
            return str(params[param])
                
        return re.sub(r'(<([^>:]+:)?(?P<param>[^>]+)>)', repl, self._path)

    def match(self, path: str) -> t.Optional[t.Dict[str, t.Any]]:
        """Check that the path is the same as the path in this route instance

        Args:
            path (str): path to check

        Returns:
            t.Optional[t.Dict[str, t.Any]]: None or a dict with params name and your value in python
        
        Examples:
            >>> route.match('/user/')
            None
            >>> route.match('/user/100')
            {'id': 100}
        """
        path = make_url(None, '/', path)

        if (_match := re.compile(self._re_path).search(path)):
            _params = {}
            for k, v in _match.groupdict().items():
                _params[k] = self._converters[k](v).to_python
            return _params
        return None

    def __eq__(self, other):
        return isinstance(other, Route) and (
            other.path == self.path and
            other.name == self.name and
            other.methods == self.methods
        )


class Router:
    def __init__(self, base_path: str = '/'):
        """Initialize a router

        Args:
            base_path (str, optional): Base path for this router. Defaults to '/'.
        
        Examples:
            >>> router = Router()
        """
        self.base_path = base_path
        self._routes: t.List[Route] = []

    def _already_exists(self, route: Route) -> bool:
        """Check if a route like this already exists on this router

        Args:
            route (Route): A route instance to check

        Returns:
            bool:
        
        Examples:
            >>> router._already_exists(Route('/404/', 'not_found', ['GET'], not_found))
            False
        """
        for _route in self._routes:
            if _route == route:
                return True
        return False

    def add_route(self, route: Route):
        """Add a route to router

        Args:
            route (Route): Route to add in this router

        Raises:
            RouteAlreadyExists: This exact route already exists or another one with the same name or path
        
        Examples:
            >>> router.add_route(Route('/', 'home', ['GET'], home_function))
            >>> router.add_route(Route('/user/<int:id>/', 'get_user', ['GET'], get_user_function))
            >>> router.add_route(Route('/user/<int:id>/', 'get_user', ['GET'], get_user_function))
            Traceback (most recent call last):
            ...
            lespy.exceptions.RouteAlreadyExists
        """
        route.path = make_url(None, self.base_path, route.path)
        if self._already_exists(route):
            raise RouteAlreadyExists
        
        self._routes.append(route)

    def find_by_name(self, name: str) -> Route:
        """Return a route with this name

        Args:
            name (str): name route to search

        Raises:
            RouteNotFound: A route with this name does not exist

        Returns:
            Route:
        
        Examples:
            >>> router.find_by_name('get_user')
            <lespy.core.router.Route object at ...>
            >>> router.find_by_name('get_me')
            Traceback (most recent call last):
            ...
            lespy.exceptions.RouteNotFound
        """
        for route in self._routes:
            if route.name == name:
                return route
        raise RouteNotFound

    def match(self, path: str, method: str) -> t.Tuple[Route, t.Dict[str, t.Any]]:
        """Finds a route based on the request path"""
        for route in self._routes:
            if method.upper() in route.methods:
                if (_match := route.match(path)) is not None:
                    return route, _match
        raise RouteNotFound
