#!/usr/bin/env python
import socket
from Drone import * 
import argparse
import threading
 

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()


class BoardComputer():

	def __init__(self,port=50010,address='192.168.1.86'):
		print("Creation of SimpleSocket instance")

		#Create a TCP/IP socket
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		#Bind the socket to the port
		server_address=(address,port)
		print ('starting up on %s port %s' % server_address)
		self.sock.bind(server_address)

		#Listen for incomimg connection
		self.sock.listen(1)
		self.connection=None
		#self.drone=drone
	
	
	#def __del__(self):
	#	print("Delete")

	def connect(self):
		#Wait for a connection
		print("Waiting for a connection")
		self.connection,client_address=self.sock.accept()
		print ('Connection from', client_address)


	def listener_loop(self):
		print("Start Listener")
		while True:
				if self.connection is None:
					print("Reconnect...")
					self.connect()
	
				else:
					data = self.connection.recv(1024)
					target = data.decode()
					print('Received "%s"' % target)

		

if __name__=="__main__":
	print("Begin of the programm")
	# Connect to the Vehicle
	#print 'Connecting to vehicle on: %s' % args.connect
	#pixhawk = connect(args.connect, baud=115200, wait_ready=True)
	#print("INITIALIZATION FINISHED")
	Nvidia=BoardComputer()
	#drone=Drone(pixhawk)
	#drone.set_mode("GUIDED")
	Nvidia.listener_loop()


