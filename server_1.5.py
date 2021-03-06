"""server_1.5.py

Now can use a future with a yield from -- fully async!
"""
# PEP8 eat your heart out
from socket import *
from fib import fib

from collections import deque

# way of watching sockets for read and write signals... (sort of an os
# level polling of the registered sockets)
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from concurrent.futures import ProcessPoolExecutor as Pool
from concurrent.futures import as_completed
pool = Pool(4)

class Loop:
    def __init__(self):
        self.ready = deque()
        self.selector = DefaultSelector()
        self.futures = {}
    def create_task(self, task):
        self.ready.append(task)
    def run_forever(self):
        while True:

            while not self.ready:
                completed_futures = [future for future in self.futures if not future.running()]
                for future in completed_futures:
                    self.ready.append(self.futures.pop(future))

                # so select() is blocking. If set a negative time out it won't block.
                events = self.selector.select(-1)
                # add these socket events and unregister them from listened to:
                for key, _ in events:
                    self.ready.append(key.data) # add the task to the ready queue
                    self.selector.unregister(key.fileobj)

            while self.ready:
                self.current_task = self.ready.popleft()
                # try to run current_task...
                try:
                    # run task to next yield point
                    reason, what = next(self.current_task)
                    if reason == 'waiting_to_accept':
                        self.selector.register(what, EVENT_READ, self.current_task)
                    elif reason == 'waiting_to_read':
                        self.selector.register(what, EVENT_READ, self.current_task)
                    elif reason == 'waiting_to_write':
                        self.selector.register(what, EVENT_WRITE, self.current_task)
                    elif reason == 'waiting_for_future':
                        self.futures[what] = self.current_task
                    else:
                        raise RuntimeError(
                            'Something bad happened... er. reason={}'.format(reason))
                except StopIteration:
                    pass

    def sock_recv(self, sock, maxbytes):
        # wait to read from the socket
        yield from read_wait(sock)
        return sock.recv(maxbytes)
    def sock_accept(self, sock):
        # wait to read/hear from the socket
        yield from accept_wait(sock)
        return sock.accept()
    def sock_sendall(self, sock, data):
        while data:
            # wait to be able to write to the socket
            yield from write_wait(sock)
            nsent = sock.send(data)
            data = data[nsent:]

    def run_in_executor(self, executor, func, *args):
        return executor.submit(func, *args)

from types import coroutine

@coroutine
def future_wait(future):
     yield 'waiting_for_future', future
     return future.result()

@coroutine
def write_wait(sock):
    yield 'waiting_to_write', sock

@coroutine
def accept_wait(sock):
    yield 'waiting_to_accept', sock

@coroutine
def read_wait(sock):
    yield 'waiting_to_read', sock

loop = Loop()
def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)     # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Running fib_server. Yay!")
    while True:
        client, addr = yield from loop.sock_accept(sock) # BLOCKING I/O
        print("Connection to client at address: ", addr)
        loop.create_task(fib_handler(client))

def fib_handler(client):
    while True:
        req = yield from loop.sock_recv(client, 100) # BLOCKING I/O
        if not req:
            break
        n = int(req)
        future = loop.run_in_executor(pool, fib, n)
        result = yield from future_wait(future)
        resp = str(result).encode('utf-8') + b'\n'
        yield from loop.sock_sendall(client, resp) # BLOCKING I/O
    print("Closed connection to client")

loop.create_task(fib_server(("", 25000)))
loop.run_forever() # run the server
