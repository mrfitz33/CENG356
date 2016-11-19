#!/usr/bin/env python

import socket

def main():
	# Create socket and its parameters
	s = socket.socket()
	host = socket.gethostname()
	port = 59426

	# Connect to the server
	s.connect((host, port))

	# Msg to start winning number generation
	s.send("start generating winning number")

	# Create a list for the digits of the winning number
	winning_num = []
	
	#print(s.recv(1024))

	while True:
		if s.recv(1024) == "ready to send digit":
			s.send("ready to receive digit")
			winning_num.append(int(s.recv(1024)))
			print(''.join(str(winning_num)))
			s.send("received digit")	
		
	# Close the connection
	s.close()

if __name__ == "__main__":
	main()

