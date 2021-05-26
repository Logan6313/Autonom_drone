#!/usr/bin/env python

import socket
from time import sleep

 
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Bind the socket to the port
server_address = ('192.168.1.86',50007)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)
 
# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print('Waiting for a connection')
connection, client_address = sock.accept()
print ('Connection from', client_address)

while True:

	data = connection.recv(1024)
	dec_data = data.decode()
	print('Received "%s"' % dec_data)
	mes = "bien recu"
	connection.send(mes.encode())

           
# Clean up the connection
connection.close()
