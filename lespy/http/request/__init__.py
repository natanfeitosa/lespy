import typing as t

from lespy.http.request.base import RequestBase
from lespy.http.utils import parse_qs, _PRIMITIVES


class Request(RequestBase):
    def __init__(self, environ: t.Dict[str, t.Any]):
        self._environ = environ
        self.path = environ.get('PATH_INFO', '/')

    def _get_method(self) -> str:
        return self._environ['REQUEST_METHOD'].upper()

    def _get_scheme(self) -> str:
        return str(self._environ.get('wsgi.url_scheme'))
    
    @property
    def META(self) -> t.Dict[str, t.Any]:
        return self._environ or super().META

    @property
    def GET(self) -> t.Mapping[str, t.Union[_PRIMITIVES, t.List[_PRIMITIVES]]]:
        return parse_qs(self._environ['QUERY_STRING'])
