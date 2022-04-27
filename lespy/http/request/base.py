import typing as t

from lespy.confs import CONFIGS
from lespy.exceptions import DisallowedHost
from lespy.http.utils import make_url, _PRIMITIVES


class RequestBase:
    path: str
    PARAMS: t.Optional[t.Dict[str, t.Any]]
    
    def __init__(self):
        pass
    
    def __setattr__(self, name: str, value: t.Any) -> None:
        object.__setattr__(self, name, value)

    def _get_method(self) -> str:
        raise NotImplementedError

    @property
    def method(self) -> str:
        return self._get_method()

    def _get_host(self) -> str:
        if 'HTTP_HOST' in self.META:
            return self.META['HTTP_HOST']
        
        host = self.META['SERVER_NAME']
        if (server_port := self._get_port()) not in ('443', '80'):
            host = '%s:%s' % (host, server_port)
        return host

    @property
    def host(self) -> str:
        host = self._get_host()

        alloweds = CONFIGS.ALLOWED_HOSTS

        if len(alloweds) < 1:
            alloweds = ['.localhost', '127.0.0.1', '[::1]']
            
        _host = host.split(':')[0]
        for a in alloweds:
            if (
                a == '*' or
                a.startswith('.') and _host.endswith(a)
                or a == _host
            ):
                return host
        raise DisallowedHost

    def _get_port(self) -> str:
        if 'HTTP_X_FORWARDED_PORT' in self.META:
            port = self.META['HTTP_X_FORWARDED_PORT']
        else:
            port = self.META['SERVER_PORT']
        return str(port)

    @property
    def port(self) -> str:
        if not (port := self._get_port()):
            port = 443 if self.is_secure else 80 # type: ignore
        return str(port)

    def _get_scheme(self) -> str:
        raise NotImplementedError

    @property
    def scheme(self) -> str:
        header, secure = CONFIGS.SECURE_SSL_HEADER
        if None not in (header, secure):
            if (header_value := self.META.get(header)):
                header_value = header_value.split(',', 1)[0]
                return header_value.strip()
        if header != 'HTTP_X_FORWARDED_PROTO' and hasattr(self.META, 'HTTP_X_FORWARDED_PROTO'):
            return str(self.META.get('HTTP_X_FORWARDED_PROTO'))
        return self._get_scheme()

    @property
    def is_secure(self) -> bool:
        """True if the request was made with a secure protocol."""
        return self.scheme in ('https', 'wss')

    @property
    def original_url(self) -> str:
        return make_url(self.scheme, self.host, self.path, self.GET)

    @property
    def COOKIES(self) -> t.Dict[str, t.Any]:
        pass
                
    @property
    def META(self) -> t.Dict[str, t.Any]:
        pass
    
    @property
    def POST(self) -> t.Dict[str, t.Any]:
        pass
        
    @property
    def GET(self) -> t.Mapping[str, t.Union[_PRIMITIVES, t.List[_PRIMITIVES]]]:
        pass
        
