"""
SSL implementation of socketserver.TCPServer

Attempts to be a drop in replacement for:

socketserver.TCPServer
socketserver.ThreadingTCPServer
socketserver.ForkingTCPServer
"""
import os
import ssl
import logging
import socketserver
from typing import Type
from concurrent import futures


class TCPServer(socketserver.TCPServer):
    """ SSL implementation of socketserver.TCPServer """

    def __init__(self, server_address: tuple[str, int],
                 RequestHandlerClass: Type[socketserver.BaseRequestHandler],
                 bind_and_activate: bool = True, context: ssl.SSLContext | None = None):
        """ Wrap socket in SSL """
        socketserver.TCPServer.__init__(
            self, server_address, RequestHandlerClass, bind_and_activate=False
        )

        # Overwrite socket with it's ssl counterpart
        if context:
            self.socket = context.wrap_socket(self.socket, server_side=True)
        else:
            logging.warning("No context provided, TCPServer will run without SSL.")

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise


class ThreadingTCPServer(socketserver.ThreadingMixIn, TCPServer):
    """ ThreadingMixIn added to SSL TCPServer """


if hasattr(os, "fork"):
    class ForkingTCPServer(socketserver.ForkingMixIn, TCPServer):
        """ ForkingMixIn added to SSL TCPServer """


# ThreadPool implementation (not from socketserver)

class ThreadPoolMixIn(socketserver.ThreadingMixIn):
    """ Use a ThreadPool instead of one thread per connection """

    executor: futures.ThreadPoolExecutor = futures.ThreadPoolExecutor()
    future_threads: list[futures.Future] = []

    def process_request(self, request, client_address) -> None:
        """ Add request to process pool """
        self.future_threads.append(
            self.executor.submit(self.process_request_thread, request, client_address)
        )

    def server_close(self):
        """ Shutdown executor """
        super().server_close()
        self.executor.shutdown()
