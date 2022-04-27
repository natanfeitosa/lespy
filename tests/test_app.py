from lespy import JSONResponse, Request, App

def test_app(app: App):
    assert app._app_name == 'app1'
    assert app._base_path == '/'

def index(req: Request):
    if req.method == 'GET':
        return 'Hello, this is my first app'
            
    if req.method == 'POST':
        return JSONResponse({'err': True})

def test_get(app: App):
    app.route('/', ['GET'])(index)

    environ = {
        'PATH_INFO': '/',
        'REQUEST_METHOD': 'GET'
    }

    headers = []

    def start_response(*a):
        nonlocal headers
        headers = a
    res = app(environ, start_response)

    assert list(res)[0] == b'Hello, this is my first app'
    assert headers[0] == '200 OK'
    assert ('Content-Type', 'text/plain') in headers[1]

def test_post(app: App):
    app.route('/', ['POST'])(index)

    environ = {
        'PATH_INFO': '/',
        'REQUEST_METHOD': 'POST'
    }

    headers = []

    def start_response(*a):
        nonlocal headers
        headers = a
    res = app(environ, start_response)

    assert list(res)[0] == b'{"err": true}'
    assert headers[0] == '200 OK'
    assert ('Content-Type', 'application/json') in headers[1]

def test_empty_router(app: App):
    environ = {
        'PATH_INFO': '/',
        'REQUEST_METHOD': 'GET'
    }

    headers = []

    def start_response(*a):
        nonlocal headers
        headers = a
    res = app(environ, start_response)

    assert list(res)[0] == b'Page not found.'
    assert headers[0] == '404 Not Found'
    assert ('Content-Type', 'text/html; charset=utf-8') in headers[1]

def test_route_names(app: App):
    @app.route('/', ['GET'])
    def index(req): pass

    @app.route('/register', ['POST'], 'register')
    def _index(req): pass

    assert len(app._router._routes) == 2
    assert app._find_rule('', 'get')[0].name == 'index'
    assert app._find_rule('register/', 'post')[0].name == 'register'
