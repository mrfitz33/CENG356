#!/usr/bin/env python

import socket
import thread
import random
import sys

def main():
	# Create socket object and its parameters (address and port)
	s = socket.socket()
	host = socket.gethostname()
	port = 59426

	# Allow port to be reused after ending execution
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Binding socket to an address
	s.bind((host, port))

	# Listening at address
	s.listen(5)	

	while True:
		# Accepting incoming connections
		c, addr = s.accept()
	
		# Creating new thread. Calling clientthread function for this function and passing c as argument	
		thread.start_new_thread(clientthread,(c,)) # Start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function
	
	# Close the connection
	c.close()
	s.close()
			

def clientthread(c):
	# Create lists for the digits of the winning number along with a copy of these digits, and the guessed number's digits
	winning_num = []
	winning_num_cpy = []
	guessed_num = []
	# Keep track of guesses remaining
	countdown = 10
	
	# Infinite loop so that function doesn't terminate and thread doesn't end
	while True:
		msg = c.recv(1024) # Wait until message is received then decide what to do

		# Generates 4 unique digits and adds the digits to a list (the winning number)
		if msg == "start generating winning number":
			for i in range(0, 4):
				temp_digit = (random.randint(0, 9))
				while not(winning_num.count(temp_digit) == 0):
					temp_digit = (random.randint(0, 9))
				
				winning_num.append(temp_digit)
			c.send("successfully generated winning number")	 
			#print (''.join(map(str, winning_num)))
		elif msg == "sending guessed number":
			c.send("receiving guessed number")
			# Receive the guessed number
			guessed_num = [int(j) for j in c.recv(1024)]
			#print (''.join(map(str, guessed_num)))

			# Copy the winning number into a seperate list 
			winning_num_cpy = list(winning_num)

			num_right, num_right_spot = 0, 0
			# Determine level of correctness of guess
			for j in range(0, 4):
				if winning_num[j] == guessed_num[j]:
					num_right_spot += 1
				if guessed_num[j] in winning_num_cpy:
					num_right += 1
					# remove digits in the winning number that are in the guessed number
					winning_num_cpy.remove(guessed_num[j])
			# Notify the client that the user won and close this thread
			if num_right_spot == 4:
				c.send("win")
				return None
			
			countdown -= 1
			# Notify the client that the user lost, send the winning number, and close this thread
			if countdown == 0:
				c.send("lose")
				c.recv(1024)
				c.send(''.join(map(str, winning_num)))
				return None
			# Send the results of guess
			c.send(str(num_right))
			c.recv(1024)
			c.send(str(num_right_spot))
			c.recv(1024)
			c.send(str(countdown))
		# Close the thread if user quit the client
		elif msg == "quitting program":
			print("Closing a client.")
			return None
		else:
			sys.exit("Network error. Exiting program.")
		

if __name__ == "__main__":
	main()
