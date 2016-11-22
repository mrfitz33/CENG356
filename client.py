#!/usr/bin/env python

import socket
import re
import sys

def main():
	# Create socket object and its parameters (address and port)
	s = socket.socket()
	host = socket.gethostname()
	port = 59426

	# Connect to the socket
	s.connect((host, port))

	# Msg to start winning number generation
	s.send("start generating winning number")
	
	# Checks that random number has been generated
	msg = s.recv(1024)
	if msg == "successfully generated winning number":
		pass
	else:
		sys.exit("Network error. Exiting program.")

	print "Welcome to MASTERMIND!"
		
	# Infinite loop to keep client running
	while True:
		# Receives keyboard input from user
		try:
			input = raw_input("Please guess a 4 digit number.\n Enter 'quit' to quit the game")
		except KeyboardInterrupt:
			print("Thanks for playing!")
			s.send('quitting program')
			sys.exit()

		if re.match(r'quit', input):
			print("Thanks for playing!")
			s.send("quitting program")
			sys.exit()
		if not re.match(r'\d{4}\b', input):
			print "Incorrect input. Please try again."
		else:
			s.send("sending guessed number")
			msg = s.recv(1024)
			if msg == "receiving guessed number":
				# Sends guessed number to server
				s.send(input)
			else:
				sys.exit("Network error. Exiting program.")			
		
	# Close the connection
	s.close()

if __name__ == "__main__":
	main()
