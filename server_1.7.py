"""server_1.6.py

Let's swap out for asyncio
"""
# PEP8 eat your heart out
from socket import *
from fib import fib
from concurrent.futures import ProcessPoolExecutor as Pool
pool = Pool(4)
import asyncio


# loop = Loop()
loop = asyncio.get_event_loop()

async def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)     # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    print("Running fib_server. Yay!")
    while True:
        client, addr = await loop.sock_accept(sock) # BLOCKING I/O
        print("Connection to client at address: ", addr)
        loop.create_task(fib_handler(client))

async def fib_handler(client):
    while True:
        req = await loop.sock_recv(client, 100) # BLOCKING I/O
        if not req:
            break
        n = int(req)
        future = loop.run_in_executor(pool, fib, n)
        # result = await future_wait(future)
        result = await future
        resp = str(result).encode('utf-8') + b'\n'
        await loop.sock_sendall(client, resp) # BLOCKING I/O
    print("Closed connection to client")

loop.create_task(fib_server(("", 25000)))
loop.run_forever() # run the server
