"""server_0.3.py

Where are we blocking?

"""
# PEP8 eat your heart out
from socket import *
from fib import fib

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
