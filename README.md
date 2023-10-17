# sslserver  
  
sslserver adds SSL support for classes in socketserver  
  
## Installation  
  
```pip install git+https://github.com/Y4hL/sslserver```  
  
## sslserver Objects  
  
### sslserver.TCPServer  
  
sslserver.TCPServer attempts to be a dropin replacement for the socketserver.TCPServer class. The only change is a added parameter context.  
  
class TCPServer(server_address, RequestHandlerClass, bind_and_activate=True, context=None)  
  
Passing context a valid SSLContext object will enable SSL on the server.  
If context is not passed, a warning will be logged, but the server will run without SSL.  
  
### sslserver.ThreadingTCPServer  
  
sslservers.ThreadingTCPServer is a copy of socketserver.ThreadingTCPServer but inherited from sslservers.TCPServer.  
  
### sslserver.ForkingTCPServer  
  
sslserver.ForkingTCPServer is a copy of socketserver.ForkingTCPServer but inherited from sslservers.TCPServer.  
  
## Examples  
  
TCPServer example from the [python documentation](https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example) using sslserver  
  
```python
import ssl
import sslserver
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self.data}")
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    address = ("localhost", 9999)

    # Create default SSLContext
    ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.cert", "server.key")

    # Create the server, binding to localhost on port 9999
    with sslserver.TCPServer(address, MyTCPHandler, context=context) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
```  
  
