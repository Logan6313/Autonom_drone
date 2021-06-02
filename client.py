#!/usr/bin/env python

import socket
from time import sleep

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Connect the socket to the port where the server is listening
server_address = ('192.168.1.86', 50010)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)
 

# Send data
while True:
	message = raw_input ('->')
	enc_mes = message.encode()
	print('Sending "%s"' % message)
	sock.send(enc_mes)
	sleep(1)

print('Closing socket')
sock.close()

