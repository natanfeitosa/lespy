import logging
import socket
import socketserver

from io import BytesIO
from http import HTTPStatus
from wsgiref import simple_server

from lespy import __version__
from lespy.utils import ansi_style

logger = logging.getLogger('lespy.server')

class LimitedStream:
    """Wrap another stream to disallow reading it past a number of bytes."""

    def __init__(self, stream, limit):
        self.stream = stream
        self.remaining = limit
        self.buffer = b''

    def _read_limited(self, size=None):
        if size is None or size > self.remaining:
            size = self.remaining
        if size == 0:
            return b''
        result = self.stream.read(size)
        self.remaining -= len(result)
        return result

    def read(self, size=None):
        if size is None:
            result = self.buffer + self._read_limited()
            self.buffer = b''
        elif size < len(self.buffer):
            result = self.buffer[:size]
            self.buffer = self.buffer[size:]
        else:
            result = self.buffer + self._read_limited(size - len(self.buffer))
            self.buffer = b''
        return result

    def readline(self, size=None):
        while b'\n' not in self.buffer and (size is None or len(self.buffer) < size):
            if size:
                chunk = self._read_limited(size - len(self.buffer))
            else:
                chunk = self._read_limited()
            if not chunk:
                break
            self.buffer += chunk
        sio = BytesIO(self.buffer)
        if size:
            line = sio.readline(size)
        else:
            line = sio.readline()
        self.buffer = sio.read()
        return line


class ServerHandler(simple_server.ServerHandler):
    http_version = '1.1'
    server_software = f'LESPY/{__version__}'

    def __init__(self, stdin, stdout, stderr, environ, **kwargs):
        try:
            content_length = int(environ.get('CONTENT_LENGTH'))
        except (ValueError, TypeError):
            content_length = 0
        super().__init__(
            LimitedStream(stdin, content_length), stdout, stderr, environ, **kwargs
        )

    def cleanup_headers(self):
        super().cleanup_headers()
        if 'Content-Length' not in self.headers:
            self.headers['Connection'] = 'close'
        elif not isinstance(self.request_handler.server, socketserver.ThreadingMixIn):
            self.headers['Connection'] = 'close'
        if self.headers.get('Connection') == 'close':
            self.request_handler.close_connection = True

    def close(self):
        self.get_stdin()._read_limited()
        super().close()


class WSGIRequestHandler(simple_server.WSGIRequestHandler):
    protocol_version = 'HTTP/1.1'
    server_version = f'LESPY/{__version__}'

    def address_string(self):
        return self.client_address[0]

    def log_request(self, code, size):
        if isinstance(code, HTTPStatus):
            code = code.value

        msg = f'"{self.requestline}" {code} {size}'

        if code[0] == "1":  # 1xx - Informational
            msg = ansi_style(msg, "bold")
        elif code == "200":  # 2xx - Success
            msg = ansi_style(msg, "bold", "green")
        # elif code == "304":  # 304 - Resource Not Modified
        #     msg = ansi_style(msg, "cyan")
        elif code[0] == "3":  # 3xx - Redirection
            msg = ansi_style(msg, "cyan")
        # elif code == "404":  # 404 - Resource Not Found
        #     msg = ansi_style(msg, "yellow")
        elif code[0] == "4":  # 4xx - Client Error
            msg = ansi_style(msg, "bold", "red")
        else:  # 5xx, or any other response
            msg = ansi_style(msg, "bold", "magenta")

        # [21/Apr/2022 02:10:04] "GET /admin/ HTTP/1.1" 302 0

        print(f" {ansi_style('-', 'bold')} [{self.log_date_time_string()}] {msg}")
            
    def get_environ(self):
        for k in self.headers:
            if '_' in k:
                del self.headers[k]

        return super().get_environ()

    def handle(self):
        self.close_connection = True
        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()
        try:
            self.connection.shutdown(socket.SHUT_WR)
        except (AttributeError, OSError):
            pass

    def handle_one_request(self):
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request():
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self 
        handler.run(self.server.get_app())
