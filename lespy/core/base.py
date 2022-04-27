import typing as t

from lespy.http.request import Request
from lespy.http.response.base import ResponseBase
from lespy.http.response import Response, JSONResponse
from lespy.core.router import Route
from lespy.confs import MIDDLEWARES
from lespy.exceptions import RouteNotFound

class Base:
    def __init__(self):
        pass

    def __call__(self, environ, start_response) -> ResponseBase:

        request = Request(environ)
        request.url_for = self.url_for
        
        response = self._get_response(request)

        start_response(response.full_status, response.headers)
        return response

    def _get_response(self, request: Request) -> ResponseBase:
        try:
            route, params = self._find_rule(request.path, request.method)
            request.PARAMS = params
        except RouteNotFound:
            response = Response('Page not found.', status_code=404)
        except:
            response = Response('Internal error.', status_code=500)
        else:
            if isinstance((response := route.callback(request)), (int, str)):
                response = Response(str(response), content_type='text/plain')
            elif isinstance(response, (dict, list)):
                response = JSONResponse(response)
        
        return self._resolve_middlewares('response', request, response) # type: ignore
        
    def _resolve_middlewares(self, step: str, req: Request, res: t.Optional[ResponseBase] = None) -> t.Union[Request, ResponseBase]:
        _is_res = step == 'response'

        if (middlewares := MIDDLEWARES.get_middlewares(step)):
            for middleware in middlewares:
                if _is_res:
                    res = middleware(req, res)
                    continue
                req = middleware(req)
        
        return res if _is_res else req # type: ignore

    def _find_rule(self, path: str, method: str) -> t.Tuple[Route, t.Dict[str, t.Any]]:
        raise NotImplementedError

    def url_for(self, name: str, **params) -> str:
        raise NotImplementedError
