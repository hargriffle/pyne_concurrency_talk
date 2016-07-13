"""
 a really simple netcat like client for connecting to our server

This client wants to prompt the user for a number and then sends it to the server and waits for response.

This is not concurrent!

"""

from socket import *

def fib_client(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    print("client has made connection to {} on {}".format(host, port))
    while True:
        n = int(input("Which fibonaci number would you like? "))
        sock.sendall(str(n).encode('utf-8'))
        reply = sock.recv(100)
        print("Your fib number is " + reply.decode('utf-8'))
    sock.close()

fib_client("localhost", 25000)
