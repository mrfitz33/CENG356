#!/usr/bin/env python

import socket
import random

def main():
	# Create socket and its parameters
	s = socket.socket()
	host = socket.gethostname()
	port = 59426

	# Allow port to be reused after ending execution
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind to the port
	s.bind((host, port))

	# Wait for client connection
	s.listen(5)

	# Create a list for the digits of the winning number
	winning_num = []

	while True:
		# Establish connection with client
		c, addr = s.accept()
		print "Connected to client"

		if c.recv(1024) == "start generating winning number":
			print "Sending to client"
			for i in range(0, 4):
				c.send("ready to send digit")
				if c.recv(1024) == "ready to receive digit":
					winning_num.append(random.randint(0, 9))
					c.send(str(winning_num[i]))
					if c.recv(1024) == "received digit":
						pass 

	# Close the connection
	c.close()

if __name__ == "__main__":
	main()
