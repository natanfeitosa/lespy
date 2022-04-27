import json
import typing as t

from lespy.http.response.base import ResponseBase


class Response(ResponseBase):
    _content: bytes
    
    def __init__(self, content: str, **opts):
        ResponseBase.__init__(self, **opts)
        self.content = content # type: ignore

    @property
    def content(self) -> bytes:
        return self._content

    @content.setter
    def content(self, content: str):
        self._content = self.make_bytes(content)
        self._headers['Content-Length'] = str(len(content))

    def __iter__(self) -> t.Iterator[bytes]:
        yield self.content


class JSONResponse(Response):
    def __init__(
        self,
        data: dict,
        json_dumps_params: t.Dict[str, t.Any] = {},
        **opts
    ):
        opts.setdefault('content_type', 'application/json')
        
        Response.__init__(
            self,
            json.dumps(data, **json_dumps_params),
            **opts
        )
