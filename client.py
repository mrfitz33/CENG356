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

	# Set maximum number of guesses
	guesses = 10

	# Print introduction message and instructions
	print "Welcome to MASTERMIND!"
	print "The goal of the game is to guess the winning number, a 4 digit number with no repeating digits."
	print "After every incorrect guess, the game will output the number of digits found in both the guessed and winning numbers, distinguishing between how many are in the correct versus incorrect spot."
	print "If you pick the correct 4 digit number within the max allowed number of guesses then you win the game, otherwise you lose."
	print "You have ", guesses, " guesses to win.\n"
		
	# Infinite loop to keep client running
	while True:
		# Receives keyboard input from user
		try:
			input = raw_input("Please guess a 4 digit number.\nEnter 'quit' to quit the game.\n")
		# Exit the game without exception if the user presses CTRL+C
		except KeyboardInterrupt:
			print("\nThanks for playing!")
			s.send('quitting program')
			sys.exit()
		# Exit the game if the user types 'quit'
		if re.match(r'quit$', input):
			print("\nThanks for playing!")
			s.send("quitting program")
			sys.exit()
		# Print an error message if user doesn't input a 4 digit number or 'quit'
		if not re.match(r'\d{4}$', input):
			print "\nIncorrect input. Please try again."
			print "You have ", guesses, " guesses remaining.\n"
		# Handle guessed number
		else:
			s.send("sending guessed number")
			msg = s.recv(1024)
			if msg == "receiving guessed number":
				# Sends guessed number to server
				s.send(input)
				# Receive results of guess and print them
				str = s.recv(1024)
				if str == "win":
					print('\nYou win!!')
					sys.exit()
				elif str == "lose":
					print("\nYou lose!!")
					s.send("ask for winning number")
					print'The winning number was ', s.recv(1024)
					sys.exit()
				else:
					print'\nYou have ', str, ' correct digits.'
					s.send("random")
					print'You have ', s.recv(1024), ' digits in the right spot.'
					s.send("random")
					guesses = s.recv(1024)
					print'You have ', guesses, ' guesses remaining.\n'
			else:
				sys.exit("Network error. Exiting program.")			
		
	# Close the connection
	s.close()

if __name__ == "__main__":
	main()
