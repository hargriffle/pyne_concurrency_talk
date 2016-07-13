"""server_0.4.py

Now we're going to make our event loop

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

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)     # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Running fib_server. Yay!")
    while True:
        client, addr = sock.accept() # BLOCKING I/O
        print("Connection to client at address: ", addr)
        fib_handler(client)

def fib_handler(client):
    while True:
        req = client.recv(100) # BLOCKING I/O
        if not req:
            break
        n = int(req)
        resp = str(fib(n)).encode('utf-8') + b'\n'
        client.send(resp) # BLOCKING I/O
    print("Closed connection to client")

fib_server(("", 25000))
