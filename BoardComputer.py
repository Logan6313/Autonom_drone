#!/usr/bin/env python
import socket
from Drone import * 
import argparse
import threading
 
"""
Created on May 18 2021

@author: Logan Robert
Interface between ground station control and the flight controller inside the drone
"""

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
		""" ---------------------
		   Connection between ground control computer and on-board computer
			--------------------
		"""
	
		print("Waiting for a connection")
		self.connection,client_address=self.sock.accept()
		print ('Connection from', client_address)

	def close(self):
		""" ---------------------
		   Close the connection between ground control computer and on-board computer
			--------------------
		"""
		print("Close socket")
		self.sock.shutdown(socket.SHUT_RDWR)
   		self.sock.close()
	
	def check_decode_int(self,data):
		""" ---------------------
		   Check if the data (string) is a number(int) or not
			--------------------
		"""
		if data.isdigit()==True:
			return True
		else:
			return False

	def check_decode_float(self,data):
		""" ---------------------
		   Check if the data (string) is a number(float) or not
			--------------------
		"""
		try:
		    float(data)
		    return True
		except ValueError:
		    return False
				

	def listener_loop(self):
		""" ---------------------
		   Receive data from the computer and send it informations
			--------------------
		"""
		print("Start Listener")
		mode_list=["GUIDED","AUTO","STABILIZE","LAND","RTL"]
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
							if target[1] in mode_list:
								self.drone.mode(target[1])
								self.write("Mode changed")
							else:
								self.write("No command valid")
						else:
							mode=self.drone.mode()
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
								self.write("No command valid")
						else:
							state=self.drone.arm()
							self.write("Arm ? : {}".format(state))

					elif target[0]=="is_armable" and len(target)==1 :
							state=self.drone.is_armable()
							self.write("Vehicle is armable ? {}".format(state))
					
						
					elif target[0]=="takeoff" and len(target)==2 :
						if self.check_decode_float(target[1])==True:
							self.drone.takeoff(target[1])
							self.write("Altitude reached : {} meters".format(target[1]))
						else:
							self.write("No command valid")

					elif target[0]=="land" and len(target)==1 :
							self.drone.land_here()
							self.write("Land ok")

					elif target[0]=="airspeed" and len(target)==2 :
						if self.check_decode_int(target[1])==True:
							self.drone.airspeed(target[1])
							self.write("Airspeed changed to {} m/s".format(target[1]))
						else:
							self.write("No command valid")

					elif target[0]=="alt" and len(target)==2:
						if self.check_decode_float(target[1])==True:
							self.drone.reach_altitude(target[1])
							self.write("Altitude reached : {} meters".format(target[1]))
						else:
							self.write("No command valid")

					elif target[0]=="go" and len(target)==5:
						if self.check_decode_float(target[1]) and self.check_decode_float(target[2]) and self.check_decode_float(target[3]) and self.check_decode_int(target[4])==True:
							self.drone.go_location(target[1],target[2],target[3],target[4])
							self.write("New location reached")

					elif target[0]=="home" and len(target)==4:
						if self.check_decode_float(target[1]) and self.check_decode_float(target[2]) and self.check_decode_float(target[3])==True:
							self.drone.set_home_location(target[1],target[2],target[3])
							self.write("New home location")
						else:
							self.write("No command valid")

					elif target[0]=="mission" and len(target)==1:
						self.drone.mission("mission.txt")
						self.write("Mission end")

					elif target[0]=='x'and len(target)==2:
						if self.check_decode_int(target[1])==True:
							self.drone.manual_control_x(target[1])
							self.write("Manual control x ok")
						else:
							self.write("No command valid")

					elif target[0]=='y'and len(target)==2:
						if self.check_decode_int(target[1])==True:
							self.drone.manual_control_y(target[1])
							self.write("Manual control y ok")
						else:
							self.write("No command valid")

					elif target[0]=="yaw" and len(target)==2:
						if self.check_decode_int(target[1])==True and int(target[1])>=0 and int(target[1])<=360:
								self.drone.condition_yaw(target[1])
								self.write("Manual control yaw ok")
						else:
							self.write("No command valid")
										
					elif target[0]=="vel" and len(target)==5:
						if self.check_decode_float(target[1]) and self.check_decode_float(target[2]) and self.check_decode_float(target[3]) and self.check_decode_int(target[4])==True:
							self.drone.send_global_velocity(target[1],target[2],target[3],target[4])
							self.write("Velocity changed")

					elif target[0]=="info" and len(target)==1:
						vehicle_state=self.drone.info()
						self.write("Version: {} \nHome location: {} \nLatitude: {} \nLongitude: {} \nAltitude: {}m \nYaw: {}  \nPitch: {}  \nRoll: {}  \nBattery voltage: {} mv \nBattery percent {} % ".format(vehicle_state[0],vehicle_state[1],vehicle_state[2],vehicle_state[3],vehicle_state[4],vehicle_state[5],vehicle_state[6],vehicle_state[7],vehicle_state[8],vehicle_state[9]))

					elif target[0]=="close" and len(target)==1:
						self.close()
						break

					else:
						self.write("No command valid")

					sleep(0.01)
					
		except KeyboardInterrupt :
			print("Exception occured")
			self.drone.mode("RTL")
			self.close()
				
	def write(self,msg):
		""" ---------------------
		   Send data to the ground control computer
			--------------------
		"""

		if self.connection is None:
			self.connect()
		else:
			self.connection.send(msg.encode())
		
		
if __name__=="__main__":
	print("Begin of the program")
	#Connect to the Vehicle
	print ('Connecting to vehicle on: %s' % args.connect)
	pixhawk = connect(args.connect, baud=115200, wait_ready=True)
	print("INITIALIZATION FINISHED")
	#Declarations of instance
	drone=Drone(pixhawk)
	#Nvidia=BoardComputer(drone)  #test with NVIDIA in network 1
	Nvidia=BoardComputer(drone,14550,'127.0.0.1') #test with Gazebo simulator
	#Nvidia = ('172.20.10.5', 50010) #test with NVIDIA in network 2
	Nvidia.connect()
	Nvidia.listener_loop()


