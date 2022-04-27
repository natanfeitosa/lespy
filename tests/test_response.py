from lespy import Response
from lespy.http.response import JSONResponse

def test_content(res: Response):
    
    assert [*res] == [b'Hello']
    
    res.content = b'Hi!!'
    assert res.content == b'Hi!!'

def test_status(res: Response):
    
    assert res.full_status == '200 OK'
    
    res.status_code = 100
    assert res.status_code == 100
    assert res.phrase == 'Continue'
    assert res.full_status == '100 Continue'

def test_headers(res: Response):
    
    headers = dict({k: v for k, v in res.headers})
    
    assert 'Content-Type' in headers and headers['Content-Type'] == 'text/html; charset=utf-8'
    assert 'Content-Length' in headers and headers['Content-Length'] == '5'

def test_cookies(res: Response):
    
    res.set_cookie('foo', 'bar')
    
    def _helper(name, value, *kw):
        assert res._cookies.get(name).value == value
        
        def _format(*kw) -> str:
            if len(kw) > 0:
                return '; ' + '; '.join(kw)
            return '; Path=/'
        
        assert res.headers.index(('Set-Cookie', f'{name}={value}{_format(*kw)}')) >= 0
    
    _helper('foo', 'bar')
    
    res.set_cookie('name', 'Natan', 1000, path='/about', secure=True, httponly=True)
    _helper('name', 'Natan', 'HttpOnly', 'Max-Age=1000', 'Path=/about', 'Secure')

def test_json_response():
    res = JSONResponse({'a': 1, 'b': 2})
    
    assert res.content == b'{"a": 1, "b": 2}'
