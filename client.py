#!/usr/bin/env python

import socket

s = socket.socket()
host = socket.gethostname()
port = 59426

s.connect((host, port))
print(s.recv(1024))
while True:
	pass
s.close()
