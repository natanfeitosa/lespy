import logging
import socket
import typing as t
from wsgiref import simple_server
from lespy.utils import ansi_style

logger = logging.getLogger('lespy.server')


class WSGIServer(simple_server.WSGIServer):
    """BaseHTTPServer that implements the Python WSGI protocol"""

    request_queue_size = 10

    def __init__(self, *args, ipv6=False, allow_reuse_address=True, **kwargs):
        if ipv6:
            self.address_family = socket.AF_INET6
        self.allow_reuse_address = allow_reuse_address
        super().__init__(*args, **kwargs)

def run(app: t.Callable, addr: str = '127.0.0.1', port: int = 3000, ipv6: bool = False):
    """Run an application in development mode

    Args:
        app 
    
    Examples:
        >>> app = App('core')
        >>> @app.get('/', 'Home')
        ... def f(req):
        ...    return 'Hello'
        ...
        >>> run(app) # Using default addr and port
    """
    
    from lespy.server.handlers import WSGIRequestHandler
    httpd = WSGIServer((addr, port), WSGIRequestHandler, ipv6=ipv6)
    
    httpd.set_app(app)
    _addr, _port = httpd.server_address

    msg = []
    
    msg.append(ansi_style(' * Starting development server at {schema}://{addr}:{port}/'.format(
        schema= 'http' if _port != 443 else 'https',
        addr= '[%s]' % _addr if ipv6 else _addr,
        port= port
    ), 'bold', 'magenta'))
    
    msg.append(ansi_style(' * (Press CTRL|CMD + C to quit)', 'bold', 'cyan'))

    print('\n'.join(msg), '\n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        import sys
        print(ansi_style(' Closing the development server...', 'red'))
        sys.exit(0)
