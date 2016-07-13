"""
perf2.py

Measure the number of short running requests that can be made.

"""

from socket import *
import time

sock=socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

from threading import Thread

n = 0

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0

Thread(target=monitor).start()
while True:
    sock.send(b'1')
    resp = sock.recv(100)
    n += 1
