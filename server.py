#!/usr/bin/env python

import socket

s = socket.socket()
host = socket.gethostname()
port = 59426
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

s.listen(5)
while True:
	c, addr = s.accept()
	print "Got connection from", addr
	c.send('Thank you for connecting')
	c.close()
