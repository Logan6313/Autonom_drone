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

	def airspeed(self,data):
		print("Let's change airspeed velocity !")
		self.pixhawk.airspeed=float(data)

	def groundspeed(self,data):
		print("Let's change groundspeed velocity !")
		self.pixhawk.groundspeed=float(data)

	def home_location(self):
		print("Let's get home location !")
		return self.pixhawk.home_location


	def takeoff(self,data):
		print("Let's takeoff !")

		self.arm()
		self.pixhawk.simple_takeoff(float(data))

		while True:
	  		print " Altitude: ", self.pixhawk.location.global_relative_frame.alt        
			if self.pixhawk.location.global_relative_frame.alt>=float(data)*0.95: 
			  print "Reached target altitude"
			  break
			sleep(1)

		print("Take off complete")

	def reach_altitude(self,data):
		print("Let's reach altitude: " + data)

		self.airspeed(5)
		cmds = self.pixhawk.commands
		cmds.download()
		cmds.wait_ready()

		home=self.home_location()
		
		point=LocationGlobalRelative(home.lat,home.lon,float(data))
		self.pixhawk.simple_goto(point)
		sleep(5)
		print("Altitude reach")

	def go_location(self,lat,lon,alt):
		print("Let's go to a new location !")

		self.airspeed(5)
		cmds = self.pixhawk.commands
		cmds.download()
		cmds.wait_ready()

		point=LocationGlobalRelative(float(lat),float(lon),float(alt))
		self.pixhawk.simple_goto(point)
		sleep(30)
		print("Location reach")

	def mission(self):
		print("Let's load a mission !")

if __name__=="__main__":
	print("Begin of the program")	

		

