from dronekit import *
from pymavlink import mavutil
from time import sleep


class Drone():

	def __init__(self,pixhawk):
		print("Creation of Drone instance")
		self.pixhawk=pixhawk

	def set_mode(self,data):
		print("Change flight mode")
		self.pixhawk.mode=VehicleMode(data)

	def arm(self):
		print("Let's arm !")

		while not self.pixhawk.is_armable:
			print " Waiting for vehicle to initialise..."
			time.sleep(1)
				
		print "Arming motors"
		self.set_mode("GUIDED")
		self.pixhawk.armed = True

		while not self.pixhawk.armed:
			print " Waiting for arming..."
			time.sleep(1)

	def disarm(self):
		print("Let's disarm !")
		self.pixhawk.armed=False

	def takeoff(self,data):
		print("Let's takeoff !")

	def land(self):
		print("Let's landing !")

	def speed(self,data):
		print("Let's change velocity !")

	def set_home_location(self,data):
		print("Let's change home location !")

	def go_location(self,data):
		print("Let's go to a new location !")

	def mission(self):
		print("Let's load a mission !")

if __name__=="__main__":
	print("Begin of the program")	

		

