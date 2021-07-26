#!/usr/bin/env python

import socket
from time import sleep

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Connect the socket to the port where the server is listening
#server_address = ('192.168.1.86', 50010) #test with NVIDIA in network 1
server_address = ('127.0.0.1', 14550) #test with Gazebo simulator
#server_address = ('172.20.10.5', 50010) #test with NVIDIA in network 2
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)
 

# Send data
while True:
	try:
		message = raw_input ('->')
		enc_mes = message.encode()
		print('Sending "%s"' % message)
		sock.send(enc_mes)
		data=sock.recv(4096)
		if not data:
			break
		else:
			print(data)
		sleep(0.5)

	except KeyboardInterrupt:
		message="close"
		enc_mes=message.encode()
		sock.send(enc_mes)
		break
			
print('Closing socket')
sock.close()

