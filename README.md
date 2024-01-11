# sslserver  
  
sslserver adds SSL support for classes in socketserver  
  
## Installation  
  
```pip install git+https://github.com/Y4hL/sslserver```  
  
## sslserver Objects  
  
### sslserver.TCPServer  
  
sslserver.TCPServer attempts to be a dropin replacement for the socketserver.TCPServer class. The only change is a added parameter context.  
  
```python
class TCPServer(server_address, RequestHandlerClass, bind_and_activate=True, context=None)
```  
  
Passing context a valid SSLContext object will enable SSL on the server.  
If context is not passed, a warning will be logged, but the server will run without SSL.  
  
### sslserver.ThreadingTCPServer  
  
sslservers.ThreadingTCPServer is a copy of socketserver.ThreadingTCPServer but inherited from sslservers.TCPServer.  
  
### sslserver.ForkingTCPServer  
  
sslserver.ForkingTCPServer is a copy of socketserver.ForkingTCPServer but inherited from sslservers.TCPServer.  
  
### sslserver.ThreadPoolMixIn  
  
ThreadPoolMixIn uses concurrent.futures.ThreadPoolExecutor to process requests.  
While socketserver.ThreadingMixIn creates a thread for each connection, ThreadPoolMixIn reuses a set amount of threads.  
As with socketserver.ThreadingMixIn, ThreadPoolMixIn can be used with both socketserver.TCPServer and sslserver.TCPServer  
  
## Examples  
  
### TCPServer example from the [python documentation](https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example) using sslserver  
  
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
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.cert", "server.key")

    # Create the server, binding to localhost on port 9999
    with sslserver.TCPServer(address, MyTCPHandler, context=context) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
```  
  
### ThreadPoolMixIn example  
  
```python
import sslserver
import socketserver

# Use sslserver.ThreadPoolMixIn to create new server class
# socketserver.TCPServer can be changed to sslserver.TCPServer for ssl support
class ThreadPoolTCPServer(sslserver.ThreadPoolMixIn, sslserver.TCPServer):
    """ socketserver.TCPServer using a ThreadPool """

class MyTCPHandler(socketserver.BaseRequestHandler):
    """ Handler class for incoming connections """

    def handle(self):
        self.data = self.request.recv(1024)
        print(f"{self.client_address[0]} wrote: {self.data}")
        # Send data back in uppercase
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    address = ("localhost", 9999)

    with ThreadPoolTCPServer(address, MyHandler) as server:
        server.serve_forever()
```  
  
### ThreadPoolMixIn with custom amount of threads  
  
TheadPoolMixIn by default lets concurrent.futures.ThreadPoolExecutor choose the amount of threads it uses.  
However if one wants to overwrite this value, it can be done before calling serve_forever()  
  
```python
from concurrent.futures import ThreadPoolExecutor

if __name__ == "__main__":
    address = ("localhost", 9999)

    thread_count = 32

    with ThreadPoolTCPServer(address, MyHandler) as server:
        # Overwrite executor
        server.executor = ThreadPoolExecutor(max_workers=thread_count)
        server.serve_forever()
```  
  
