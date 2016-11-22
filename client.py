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
	guesses = 10
	print "Welcome to MASTERMIND!"
	print "You have ", guesses, "  guesses to win"
		
	# Infinite loop to keep client running
	while True:
		# Receives keyboard input from user
		try:
			input = raw_input("Please guess a 4 digit number.\nEnter 'quit' to quit the game\n")
		except KeyboardInterrupt:
			print("\nThanks for playing!")
			s.send('quitting program')
			sys.exit()

		if re.match(r'quit', input):
			print("\nThanks for playing!")
			s.send("quitting program")
			sys.exit()
		if not re.match(r'\d{4}\b', input):
			print "Incorrect input. Please try again."
			print "You have ", guesses, " guesses remaining\n"
		else:
			s.send("sending guessed number")
			msg = s.recv(1024)
			if msg == "receiving guessed number":
				# Sends guessed number to server
				s.send(input)
				str = s.recv(1024)
				if str == "win":
					print('You win!!')
					sys.exit()
				elif str == "lose":
					print("You lose!!")
					sys.exit()
				else:
					print'You have ', str, ' correct numbers'
					s.send("random")
					print'You have ', s.recv(1024), ' numbers in the right spot'
					s.send("random")
					guesses = s.recv(1024)
					print'You have ', guesses, ' guesses remaining\n'
			else:
				sys.exit("Network error. Exiting program.")			
		
	# Close the connection
	s.close()

if __name__ == "__main__":
	main()
