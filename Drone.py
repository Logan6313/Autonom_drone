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



if __name__=="__main__":
	print("Begin of the programm")	

		

