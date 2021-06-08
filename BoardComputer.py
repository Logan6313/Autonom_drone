#!/usr/bin/env python
import socket
from Drone import * 
import argparse
import threading
 

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()


class BoardComputer():

	def __init__(self,drone,port=50010,address='192.168.1.86'):
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
		self.drone=drone
	
	
	#def __del__(self):
	#	print("Delete")

	def connect(self):
		#Wait for a connection
		print("Waiting for a connection")
		self.connection,client_address=self.sock.accept()
		print ('Connection from', client_address)

	def close(self):
		print("Close socket")
		self.sock.shutdown(socket.SHUT_RDWR)
   		self.sock.close()
		

	def listener_loop(self):
		print("Start Listener")
		try:
			if self.connection is None:
				self.connect()
			while True:
					data = self.connection.recv(4096)
					if not data:
						print("No data from controller")
						sleep(0.1)
						self.connect()
						break
					target = data.decode("ASCII").split(" ")
					print('Received "%s"' % target)
					if target[0]=="mode":
						if len(target)==2:
							self.drone.set_mode(target[1])
							self.write("Mode changed")
						else:
							mode=self.drone.set_mode()
							self.write("Mode : {}".format(mode))

					elif target[0] == "arm":
						if len(target)==2:
							if target[1]=="on":
								self.drone.arm(target[1])
								self.write("Vehicle armed")
							elif target[1]=="off":
								self.drone.arm(target[1])
								self.write("Vehicle disarmed")
						else:
							state=self.drone.arm()
							self.write("Arm ? : {}".format(state))
						
					elif target[0]=="takeoff":
						if len(target)==2:
							self.drone.takeoff(target[1])
							self.write("Altitude reached : {} meters".format(target[1]))

					elif target[0]=="alt":
						if len(target)==3:
							self.drone.reach_altitude(target[1],target[2])
							self.write("Altitude reached : {} meters".format(target[1]))

					elif target[0]=="go":
						if len(target)==5:
							self.drone.go_location(target[1],target[2],target[3],target[4])
							self.write("New location reached")

					elif target[0]=="home":
						if len(target)==4:
							self.drone.set_home_location(target[1],target[2],target[3])
							self.write("New home location")

					elif target[0]=="mission":
						self.drone.mission("test.txt")
						self.write("Mission end")

					elif target[0]=="close":
						self.close()
						break

					else:
						self.write("No command valid")

					sleep(0.01)
					
		except KeyboardInterrupt :
			print("Exception occured")
			self.close()
			
			


	def write(self,msg):
		self.connection.send(msg.encode())

		
		
if __name__=="__main__":
	print("Begin of the program")
	#Connect to the Vehicle
	print ('Connecting to vehicle on: %s' % args.connect)
	pixhawk = connect(args.connect, baud=115200, wait_ready=True)
	print("INITIALIZATION FINISHED")
	#Declarations of instance
	drone=Drone(pixhawk)
	Nvidia=BoardComputer(drone)
	Nvidia.connect()
	Nvidia.listener_loop()


