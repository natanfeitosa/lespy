import pytest # type: ignore

from lespy import App, Container, Response, Request

@pytest.fixture
def app() -> App:
    return App('app1')

@pytest.fixture
def container() -> Container:
    return Container()

@pytest.fixture
def res() -> Response:
    return Response('Hello')

@pytest.fixture
def req() -> Request:
    environ = {
        'wsgi.url_scheme': 'https',
        'HTTP_HOST': '127.0.0.1',
        'SERVER_PORT': '443',
        'PATH_INFO': '/',
        'QUERY_STRING': 'foo=bar',
        'REQUEST_METHOD': 'GET',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_IS_THIS_A_HEADER': 'yes',
    }
    return Request(environ)
