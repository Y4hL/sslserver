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
from typing import Type

from socketserver import ThreadingMixIn
from socketserver import TCPServer as _TCPServer
from socketserver import BaseRequestHandler


if hasattr(os, "fork"):
    from socketserver import ForkingMixIn


class TCPServer(_TCPServer):
    """ SSL implementation of socketserver.TCPServer """

    def __init__(self, server_address: tuple[str, int],
                 RequestHandlerClass: Type[BaseRequestHandler],
                 bind_and_activate: bool = True, context: ssl.SSLContext | None = None):
        """ Wrap socket in SSL """
        _TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=False)

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


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    """ ThreadingMixIn added to SSL TCPServer """


if hasattr(os, "fork"):
    class ForkingTCPServer(ForkingMixIn, TCPServer):
        """ ForkingMixIn added to SSL TCPServer """
