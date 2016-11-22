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

	# Listening at address (5 indicates number of clients allowed)
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
	# Create lists for the digits of the winning number and guessed number
	winning_num = []
	guessed_num = []
	countdown = 10
	# Infinite loop so that function doesn't terminate and thread doesn't end
	while True:
		msg = c.recv(1024) # Wait until message is received then decide what to do

		# Generates the winning number and adds the digits to a list
		if msg == "start generating winning number":
			for i in range(0, 4):
				winning_num.append(random.randint(0, 9))
			c.send("successfully generated winning number")	 
			print (''.join(str(winning_num)))
		elif msg == "sending guessed number":
			c.send("receiving guessed number")
			# Receive the guessed number
			guessed_num = [int(j) for j in c.recv(1024)]
			print ''.join(str(guessed_num))

			num_right, num_right_spot = 0, 0
			for j in range(0, 4):
				if winning_num[j] == guessed_num[j]:
					num_right_spot += 1
				if winning_num.count(guessed_num[j]):
					num_right += 1
			if num_right_spot == 4:
				c.send("win")
				return None
			
			countdown -= 1
			if countdown == 0:
				c.send("lose")
				return None
			c.send(str(num_right))
			c.recv(1024)
			c.send(str(num_right_spot))
			c.recv(1024)
			c.send(str(countdown))
		elif msg == "quitting program":
			print("quitting the program")
			return None
		else:
			sys.exit("Network error. Exiting program.")
		

if __name__ == "__main__":
	main()
