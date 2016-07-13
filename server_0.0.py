"""server_0.0.py

Let's make a fib microservice for this!
"""
from socket import * # PEP8 eat your heart out
from fib import fib

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)     # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Running fib_server. Yay!")
    while True:
        client, addr = sock.accept()
        print("Connection to client at address: ", addr)
        fib_handler(client)

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        resp = str(fib(n)).encode('utf-8') + b'\n'
        client.send(resp)
    print("Closed connection to client")

fib_server(("", 25000))
