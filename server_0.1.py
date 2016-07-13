"""

Let's add some threading!



"""
# PEP8 eat your heart out
from socket import *
from fib import fib
from threading import Thread

def fib_server(address):
    # TCP socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Running fib_server with THREADS! ")
    while True:
        client, addr = sock.accept()
        print("Connection to client at address: ", addr)
        Thread(target=fib_handler, args=(client,), daemon=True).start()

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
