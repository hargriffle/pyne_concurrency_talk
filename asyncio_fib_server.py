"""asyncio_fib_server.py

An implementation of the fib server using asyncio.
"""

from fib import fib

from socket import *
import asyncio
from concurrent.futures import ProcessPoolExecutor as Pool
pool = Pool(4)

loop = asyncio.get_event_loop()

async def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        print("Connection from", addr)
        loop.create_task(fib_handler(client))

async def fib_handler(client):
    with client:
        while True:
            req = await loop.sock_recv(client, 100)
            if not req:
                break
            n = int(req)
            future = loop.run_in_executor(pool, fib, n)
            result = await future
            resp = str(result).encode('utf-8') + b'\n'
            await loop.sock_sendall(client, resp)
    print("Connection closed to", client)

loop.create_task(fib_server(('', 25000)))
loop.run_forever() # start the server
