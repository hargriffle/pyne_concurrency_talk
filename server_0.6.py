"""server_0.5.py

Adding some socket methods to our event loop.

"""
# PEP8 eat your heart out
from socket import *
from fib import fib

from collections import deque

class Loop:
    def __init__(self):
        self.ready = deque()
    def create_task(self, task):
        self.ready.append(task)
    def run_forever(self):
        while True:
            while not self.ready:
                # hmmn, nothing to run -> must be waiting on stuff...
                pass
            while self.ready:
                self.current_task = self.ready.popleft()
                # try to run current_task...
    def sock_recv(self, sock, maxbytes):
        # wait to read from the socket
        return sock.recv(maxbytes)
    def sock_accept(self, sock):
        # wait to read/hear from the socket
        return sock.accept()
    def sock_sendall(self, sock, data):
        while data:
            # wait to be able to write to the socket
            nsent = sock.send(data)
            data = data[nsent:]


loop = Loop()
def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)     # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Running fib_server. Yay!")
    while True:
        client, addr = loop.sock_accept(sock) # BLOCKING I/O
        print("Connection to client at address: ", addr)
        fib_handler(client)

def fib_handler(client):
    while True:
        req = loop.sock_recv(client, 100) # BLOCKING I/O
        if not req:
            break
        n = int(req)
        resp = str(fib(n)).encode('utf-8') + b'\n'
        loop.sock_sendall(client, resp) # BLOCKING I/O
    print("Closed connection to client")

fib_server(("", 25000))
