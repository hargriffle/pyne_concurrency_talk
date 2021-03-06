"""server_0.9.py



"""
# PEP8 eat your heart out
from socket import *
from fib import fib

from collections import deque

# way of watching sockets for read and write signals... (sort of an os level polling of the registered sockets)
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

class Loop:
    def __init__(self):
        self.ready = deque()
        self.selector = DefaultSelector()
    def create_task(self, task):
        self.ready.append(task)
    def run_forever(self):
        while True:
            # hmmn, nothing to run -> must be waiting on stuff...
            while not self.ready:
                events = self.selector.select()
                # add these events and unregister them from listened to:
                for key, _ in events:
                    self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)
            while self.ready:
                self.current_task = self.ready.popleft()
                # try to run current_task...
                try:
                    # run task to next yield point
                    reason, sock = next(self.current_task)
                    if reason == 'waiting_to_accept':
                        # need to register this with the selector
                        self.selector.register(sock, EVENT_READ, self.current_task)
                except StopIteration:
                    pass

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
        yield 'waiting_to_accept', sock
        client, addr = loop.sock_accept(sock) # BLOCKING I/O
        print("Connection to client at address: ", addr)
        loop.create_task(fib_handler(client))

def fib_handler(client):
    while True:
        yield 'waiting_to_read', client
        req = loop.sock_recv(client, 100) # BLOCKING I/O
        if not req:
            break
        n = int(req)
        resp = str(fib(n)).encode('utf-8') + b'\n'
        yield 'waiting_to_write', client
        loop.sock_sendall(client, resp) # BLOCKING I/O
    print("Closed connection to client")

loop.create_task(fib_server(("", 25000)))
loop.run_forever() # run the server
