import typing as t
from urllib.parse import parse_qsl

from pyfunctools.utils import to_num # type: ignore

def make_url(
    scheme: t.Optional[str] = None,
    host: t.Optional[str] = None,
    path: t.Optional[str] = None,
    query_string: t.Any = None,
) -> str:
    """Make an url with bases

    Examples:
        >>> make_url('https', 'blogexample.com/', '/posts/10000/', {'a': 1, 'b': 2})
        https://blogexample.com/posts/10000/?a=1&b=2
        >>> make_url(host='blogexample.com/', path='/posts/10000/', query_string={'a': 1, 'b': 2})
        blogexample.com/posts/10000/?a=1&b=2
    """
    url = []

    def format(slice: str) -> str:
        if slice in ['', ' ', '/']:
            return '/'
        if slice[0] == '/':
            slice = slice[1:]
        if slice[-1] != '/':
            slice += '/'
        return slice

    if scheme:
        url.extend([scheme, '://'])
    if host:
        url.append(format(host))
    if path:
        if (path := format(path)) == '/' and url[-1][-1] == '/':
            path = ''
        url.append(path)

    if url == ['/', '/']:
        url = ['/']
    
    if query_string:
        if isinstance(query_string, str):
            if query_string[0] == '?':
                query_string = query_string[1:]
        elif isinstance(query_string, dict):
            _qs = []
            for k, v in query_string.items():
                if isinstance(v, list):
                    v = ','.join(v)
                _qs.append(f'{k}={v}')
            query_string = '&'.join(_qs)
        url.extend(['?', query_string])
    return ''.join(url)


_PRIMITIVES = t.Union[str, int, float, bool]
def parse_qs(qs: str) -> t.Mapping[str, t.Union[_PRIMITIVES, t.List[_PRIMITIVES]]]:
    """Parse Query Strings

    Examples:
        >>> parse_qs('a=1&b=2')
        {'a': 1, 'b': 2}
        >>> parse_qs('a=1&b=2&a=10')
        {'a': [1, 10], 'b': 2}
        >>> parse_qs('a=1&b=2&a=10&c=Hello,%20how%20are%20you?')
        {'a': [1, 10], 'b': 2, 'c': 'Hello, how are you?'}
    """
    _qs: t.Mapping[str, t.Union[_PRIMITIVES, t.List[_PRIMITIVES]]] = {}

    for k, v in parse_qsl(qs):
        try:
            v = to_num(v)
        except:
            pass
            
        if _qs.get(k, None) is not None:
            _qs_v = _qs.get(k)
            if not isinstance(_qs_v, list):
                _qs_v = [_qs_v] # type: ignore
            _qs[k] = [*_qs_v, v] # type: ignore
            continue
        
        _qs[k] = v # type: ignore
    return _qs
