from dataclasses import dataclass
from functools import cache, cached_property
from http import HTTPMethod
import logging
from pathlib import Path
import socket
import logging
import socket
import threading

STATIC_FILES_PATH = Path('./www')
INDEX_HTML_PATH = STATIC_FILES_PATH / 'index.html'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass(frozen=True)
class Request:

    request: str

    @cached_property
    def start_line(self) -> str:
        return self.request.split('\r\n', 1)[0]

    @cached_property
    def method(self) -> HTTPMethod:
        return HTTPMethod(self.start_line.split(' ', 1)[0])

    def __len__(self) -> int:
        return len(self.request)


class RequestHandler:

    ALLOWED_METHODS = frozenset([HTTPMethod.GET, HTTPMethod.HEAD])

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, connection: socket.socket, address: tuple[str, int]) -> None:
        self._logger.info(f'Handle request from {address}')
        request = self._read_request(connection)
        self._logger.debug(f'Got request: {len(request)} bytes')
        if not self._is_method_allowed:
            self._log_request_handled(address)
            connection.close()
            return
        response = self._build_response()
        self._logger.debug('Sending response')
        connection.send(response)
        self._logger.debug('Response is sent')
        self._logger.debug('Closing connection')
        connection.close()
        self._logger.debug('Connection closed')
        self._log_request_handled(address)

    def _read_request(self, connection: socket.socket) -> Request:
        request = connection.recv(1024)
        request = request.decode()
        return Request(request)

    def _is_method_allowed(self, request: Request) -> bool:
        return request.method in self.ALLOWED_METHODS
    
    def _log_request_handled(self, address: tuple[str, int]) -> None:
        self._logger.info(f'Request from {address} handled')

    @staticmethod
    @cache
    def _build_response() -> bytes:
        response = b''
        response += b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/html\r\n\r\n'
        response += INDEX_HTML_PATH.read_bytes()
        return response


class Server:

    LISTEN_BACKLOG = 1
    CLEAN_THREADS_TRIGGER_COUNTER = 1000

    def __init__(self, host: str = 'localhost', port: int = 8080) -> None:
        self._host = host
        self._port = port
        self._logger = logging.getLogger(self.__class__.__name__)
        self._socket: socket.socket | None = None
        self._request_threads = []
        self._requests_counter = 0

    def _init_socket(self) -> None:
        self._socket = socket.socket()
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._host, self._port))
        self._socket.listen(self.LISTEN_BACKLOG)
    
    def start(self) -> None:
        self._logger.info('Starting HTTP server')
        self._init_socket()
        self._logger.info(f'HTTP server started: {self._host}:{self._port}')
        self._logger.info('Ctrl-C to stop server')
        try:
            self._loop()
        finally:
            self._socket.close()
    
    def _loop(self) -> None:
        while True:
            self._logger.debug('Waiting for connection')
            connection, address = self._socket.accept()
            self._logger.debug(f'Got connection: {address}')
            self._handle_in_thread(connection, address)
            self._requests_counter += 1
            self._clean_threads()

    def _handle_in_thread(self, connection: socket.socket, address: tuple[str, int]) -> None:
        request_thread = threading.Thread(
            target=RequestHandler(), 
            args=(connection, address),
            daemon=True,
        )
        request_thread.start()
        self._request_threads.append(request_thread)

    def _clean_threads(self) -> None:
        if self._requests_counter == self.CLEAN_THREADS_TRIGGER_COUNTER:
            self._request_threads = [thread for thread in self._request_threads if thread.is_alive()]
            self._requests_counter = 0


if __name__ == "__main__":
    Server().start()
