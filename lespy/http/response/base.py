import typing as t
from http.client import responses as http_res
from http import cookies

from lespy.confs import CONFIGS


class ResponseBase:
    """A base class for all response classes"""

    _cookies: cookies.SimpleCookie = cookies.SimpleCookie()

    def __init__(
        self,
        status_code: int = 200,
        headers: t.Optional[t.Dict[str, str]] = None,
        charset: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
    ):
        """Initialize class base

        Args:
            status_code (t.Optional[int], optional): Status code of response. Defaults to 200.
            headers (t.Optional[t.Dict[str, str]], optional): Set headers of response. Defaults to None.
            charset (t.Optional[str], optional): charset encoding. Defaults to None.
            content_type (t.Optional[str], optional): content type for response. Defaults to None.

        Raises:
            ValueError: HTTP status code must be an integer from 100 to 599.
        
        Examples:
            >>> res = ResponseBase(200, {'foo': 'bar}, 'utf-8', 'text/plain')
        """
        
        if not 100 <= status_code <= 599:
            raise ValueError('HTTP status code must be an integer from 100 to 599.')
        self._status_code = status_code

        if headers is None:
            headers = {}
        self._headers = {**headers}

        if charset is None:
            charset = CONFIGS.CHARSET
        self._charset = charset
        
        if 'Content-Type' not in self._headers:
            if not content_type:
                content_type = f'text/html; charset={self._charset}'
            self._headers['Content-Type'] = content_type
    
    def __iter__(self) -> t.Iterator[bytes]:
        raise NotImplementedError

    @property
    def status_code(self) -> int:
        """Get the status code for this response
        
        Returns:
            int : status code of response in int format
        
        Examples:
            >>> res.status_code
            200
        """
        return self._status_code

    @status_code.setter
    def status_code(self, code: int) -> None:
        """Set the new status code for this response
        
        Examples:
            >>> res.status_code = 200
        """
        self._status_code = int(code)

    @property
    def phrase(self) -> str:
        """Return phrase for current status code
        
        Examples:
            >>> res.phrase
            OK

        Returns:
            str : a phrase default is 'OK'
        """
        return http_res.get(self.status_code, 'Unknown Status Code')

    @property
    def full_status(self) -> str:
        """Return the full status
        
        Example:
            >>> res.full_status
            200 OK

        Returns:
            str : a status representation on format {{ code phrase }}
        """
        return f'{self.status_code} {self.phrase}'

    @property
    def headers(self) -> t.List[t.Tuple]:
        """Get headers in WSGI format
        
        Examples:
            >>> res.headers
            [('foo', 'bar')]
        """
        return [
            *self._headers.items(),
            *(("Set-Cookie", c.output(header="").strip()) for c in self._cookies.values()),
        ]

    def set_headers(self, headers: t.Dict[str, str]):
        """Set headers for the response

        Args:
            headers (t.Dict[str, str]): headers on dict format
        
        Examples:
            >>> res.set_headers({'foo': 'bar'})
        """
        self._headers.update((headers))

    def set_cookie(
        self,
        key: str,
        value: str = '',
        max_age: t.Optional[int] = None,
        expires: t.Optional[str] = None,
        path: str = '/',
        domain: t.Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: t.Optional[str] = None
    ):
        self._cookies[key] = value
        _c = self._cookies[key]

        if max_age is not None:
            _c['max-age'] = max_age
            
        if expires is not None:
            _c['expires'] = ''
            
        if path is not None:
            _c['path'] = path
        
        if domain is not None:
            _c['domain'] = domain
        
        if secure:
            _c['secure'] = True
        
        if httponly:
            _c['httponly'] = True

        if samesite:
            if samesite.lower() not in ('lax', 'none', 'strict'):
                raise ValueError('samesite must be "lax", "none", or "strict".')
            _c["samesite"] = samesite
    
    def set_cookies(self, cookies: t.List[t.Dict[str, t.Any]]):
        """Wrapper to set a list of cookies

        Args:
            cookies (t.List[t.Dict[str, t.Any]]): List of cookies
        
        Examples:
            >>> res.set_cookies([
                {'key': 'foo', 'value': 'bar},
                {'key': 'bar', 'value': 'foo', 'path': '/whats'}
            ])
        """
        for cookie in cookies:
            self.set_cookie(**cookie)

    def del_cookie(
        self,
        key:str,
        path:str = '/',
        domain: t.Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: t.Optional[str] = None
    ) -> None:
        """Delete cookie

        Args:
            key (str): cookie name
            path (str, optional): cookie path. Defaults to '/'.
            domain (t.Optional[str], optional): cookie domain. Defaults to None.
            secure (bool, optional): is secure cookie. Defaults to False.
            httponly (bool, optional): is httponly cookie. Defaults to False.
            samesite (t.Optional[str], optional): on samesite cookie. Defaults to None.
        """
        self.set_cookie(
            key,
            max_age=0,
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            samesite=samesite
        )
    
    def make_bytes(self, value: t.Any) -> bytes:
        """Turn a value into a bytestring encoded in the output charset.
        
        Examples:
            >>> res.make_bytes('Hi')
            b'Hi'
            >>> res.make_bytes(b'Hi')
            b'Hi'
            >>> res.make_bytes(['H', 'i'])
            b"['H', 'i']"
        """
        if isinstance(value, (bytes, memoryview)):
            return bytes(value)
        if isinstance(value, str):
            return bytes(value.encode(self._charset))
        # Handle non-string types.
        return str(value).encode(self._charset)
