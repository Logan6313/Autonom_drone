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

	def set_home_location(self,lat,lon,alt):
		print("Let's set home location !")
		pos=self.pixhawk.location.global_frame
		pos.lat=float(lat)
		pos.lon=float(lon)
		pos.alt=float(alt)
		self.pixhawk.home_location=pos 

	def get_home_location(self):
		print("Let's get home location !")
		return self.pixhawk.home_location

	def current_location(self) :
		return self.pixhawk.location.global_frame


	def takeoff(self,data):
		print("Let's takeoff !")

		self.arm()
		self.pixhawk.simple_takeoff(float(data))

		while True:
	  		print " Altitude: ", self.pixhawk.location.global_relative_frame.alt        
			if self.pixhawk.location.global_relative_frame.alt>=float(data)*0.98: 
			  print "Reached target altitude"
			  break
			sleep(1)

		print("Take off complete")

	def reach_altitude(self,data,speed):
		print("Let's reach altitude: " + data)

		self.airspeed(speed)
		cmds = self.pixhawk.commands
		cmds.download()
		cmds.wait_ready()

		home=self.current_location()
		print(home)
		
		point=LocationGlobalRelative(home.lat,home.lon,float(data))
		self.pixhawk.simple_goto(point)
		while True:
			print "Altitude: ",self.pixhawk.location.global_relative_frame.alt
			if self.pixhawk.location.global_relative_frame.alt>=float(data)*0.98:
				break
			sleep(1)

		print("Reached target altitude")

	def go_location(self,lat,lon,alt,speed):
		print("Let's go to a new location !")

		self.airspeed(speed)
		cmds = self.pixhawk.commands
		cmds.download()
		cmds.wait_ready()

		point=LocationGlobalRelative(float(lat),float(lon),float(alt))
		self.pixhawk.simple_goto(point)
		while True:
			print "Location: ",self.pixhawk.location.global_relative_frame
			if self.pixhawk.location.global_relative_frame.lon>=float(lon)*0.98 and self.pixhawk.location.global_relative_frame.alt>=float(alt)*0.98:
				break
			sleep(1)

		print("Reached location")

	def mission(self):
		print("Let's load a mission !")

if __name__=="__main__":
	print("Begin of the program")	

		

