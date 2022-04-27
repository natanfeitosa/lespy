from lespy import Request

def test_method(req: Request):
    assert req.method == 'GET'
    assert req.META['REQUEST_METHOD'] == 'GET'

def test_scheme(req: Request):
    assert req.scheme == 'https'
    assert req.META['wsgi.url_scheme'] == 'https'

def test_query_string(req: Request):
    assert req.GET['foo'] == 'bar'
    assert req.META['QUERY_STRING'] == 'foo=bar'

def test_host(req: Request):
    assert req.host == '127.0.0.1'
    assert req.META['HTTP_HOST'] == '127.0.0.1'

def test_port(req: Request):
    assert req.port == '443'
    assert req.META['SERVER_PORT'] == '443'

def test_original_url(req: Request):
    assert req.original_url == 'https://127.0.0.1/?foo=bar'
    
    req.META['wsgi.url_scheme'] = 'http'
    req.META['SERVER_PORT'] = '3000'
    
    del req.META['HTTP_HOST']
    req.META['SERVER_NAME'] = '127.0.0.1'
    assert req.original_url == 'http://127.0.0.1:3000/?foo=bar'
