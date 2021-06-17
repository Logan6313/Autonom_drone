from dronekit import *
from pymavlink import mavutil
from time import sleep
import math

"""
Created on May 18 2021

@author: Logan Robert
Different methods to move the drone
"""

class Drone():

	def __init__(self,pixhawk):
		print("Creation of Drone instance")
		self.pixhawk=pixhawk

	def info(self):
		""" -----------------------------------------
		Get informations about the drone and the flight controller
		Pram : /
		Return : version of the flight controller (string)
				 home location of the drone (latitude/degrees - longitude/degrees - altitude/meters)
				 location of the drone (latitude/degrees - longitude/degrees - altitude/meters)
				 attitude of the drone (yaw/radians)
				 battery voltage (mV)
				 battery level (%)
			-----------------------------------------
		"""
		vehicle_state=[
			self.pixhawk.version,
			self.get_home_location(),
			self.pixhawk.location.global_frame.lat,
			self.pixhawk.location.global_frame.lon,
			self.pixhawk.location.global_frame.alt,
			self.pixhawk.attitude.yaw,
			self.pixhawk.attitude.pitch,
			self.pixhawk.attitude.roll,
			self.pixhawk.battery.voltage,
			self.pixhawk.battery.level]

		return vehicle_state

	def mode(self,mode=None):
	  	""" -----------------------------------------
		Change the flight mode of the drone OR Get the flight mode
		Pram : mode (string)
		Return : /
			-----------------------------------------
		"""

		print("Change flight mode")

		# get the flight mode if mode=None 
		if mode is None:
			return self.pixhawk.mode

		# change the flight mode
		else:
			self.pixhawk.mode=VehicleMode(mode)

	def arm(self,state=None):
		""" -----------------------------------------
		Arm OR Disarm OR Get the arm mode of the drone
		Pram : state (string)
		Return : /
			-----------------------------------------
		"""
	
		# get the arm mode if state=None
		if state is None:
			return self.pixhawk.armed
		
		# arm the drone if state="on"
		elif state=="on":
			print("Let's arm !")

			while not self.pixhawk.is_armable:
				print " Waiting for vehicle to initialise..."
				time.sleep(1)
					
			print "Arming motors"
			self.mode("GUIDED")
			self.pixhawk.armed = True

			while not self.pixhawk.armed:
				print " Waiting for arming..."
				time.sleep(1)

			return True

		# disarm the drone if state="off"
		elif state=="off":
			print("Let's disarm !")
			self.pixhawk.armed=False
			while not self.pixhawk.armed==False:
				print " Waiting for disarming..."
				time.sleep(1)

			return True


	def airspeed(self,data):
	 	""" -----------------------------------------
		Change the airspeed of the drone
		Pram : data (m/s)
		Return : /
			-----------------------------------------
		"""

		print("Let's change airspeed velocity !")
		self.pixhawk.airspeed=float(data)


	def groundspeed(self,data):
		""" -----------------------------------------
		Change the groundspeed of the drone
		Param : data (m/s)
		Return: /
			-----------------------------------------
		"""

		print("Let's change groundspeed velocity !")
		self.pixhawk.groundspeed=float(data)


	def set_home_location(self,lat,lon,alt):
		""" -----------------------------------------
		Change the home location of the drone
		Param : lat => new latitude (degrees)
				lon => new longitude (degrees)
				alt => new altitude (meters)
		Return : /
			-----------------------------------------
		"""

		print("Let's set home location !")
		pos=self.pixhawk.location.global_frame
		pos.lat=float(lat)
		pos.lon=float(lon)
		pos.alt=float(alt)
		self.pixhawk.home_location=pos 


	def get_home_location(self):
		""" -----------------------------------------
		Get home location of the drone
		Param: /
		Return : home location (LocationGlobal)
			-----------------------------------------
		"""
		print("Let's get home location !")
		cmds = self.pixhawk.commands
		cmds.download()
		cmds.wait_ready()
		return self.pixhawk.home_location


	def current_location(self) :
		""" -----------------------------------------
		Get current location of the drone
		Param : /
		Return : current location(LocationGlobal)
			-----------------------------------------
		"""

		return self.pixhawk.location.global_frame


	def takeoff(self,data):
		""" -----------------------------------------
		The drone takes off
		Param : data => altitude (meters) to reach during takeoff
		Return : /
			-----------------------------------------
		"""

		print("Let's takeoff !")

		self.arm("on")
		self.pixhawk.simple_takeoff(float(data))

		while True:
	  		print " Altitude: ", self.pixhawk.location.global_relative_frame.alt        
			if self.pixhawk.location.global_relative_frame.alt>=float(data)*0.98: 
			  print "Reached target altitude"
			  break
			sleep(1)

		print("Take off complete")


	def reach_altitude(self,data):
	 	""" -----------------------------------------
		The drone goes in a specific altitude remaining on site
		Param : data => altitude (meters) to reach
		Return : /
			-----------------------------------------
		"""

		print("Let's reach altitude: " + data)

		self.airspeed(5)
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
		""" -----------------------------------------
		The drone goes in a specific location choosen by the user
		Param : lat => latitude (degrees) to reach
				lon => longitude (degrees) to reach
				alt => altitude (meters) to reach
				speed => speed (m/s) where the drone will fly 
		Return : /
			-----------------------------------------
		"""

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


	def calc_distance(self,current,target):
		""" -----------------------------------------
		Method used to calculate distance between two points on Earth
		Param : current => current location of the drone (LocationGlobalRelative)
				target => traget location to reach (LocationGlobalRelative)
		Return : d => distance between the two points (meters)
			-----------------------------------------
		"""

		#Conversion degrees-radians
		c_lat=math.radians(current.lat)
		t_lat=math.radians(target.lat)
		c_lon=math.radians(current.lon)
		t_lon=math.radians(target.lon)

		#Calculation of the distance
		d=6371*math.acos(math.sin(c_lat)*math.sin(t_lat)+math.cos(c_lat)*math.cos(t_lat)*math.cos(t_lon-c_lon))
		
		return d*1000


	"""------------------MANUAL	 CONTROL--------------------"""

	def manual_control_x(self,x):
		""" -----------------------------------------
		Control the drone in position according the x axis
		Param : x => distance (meters) 
		Return : /
			-----------------------------------------
		"""

		msg = self.pixhawk.message_factory.set_position_target_local_ned_encode(
		    0,       # time_boot_ms (not used)
		    0, 0,    # target system, target component
		    mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
		    0b0000111111111000, # type_mask (only position enabled)
		    float(x), # X position
		    0, # Y Position 
		    0, # Altitude in meters 
		    0, # X velocity in NED frame in m/s
		    0, # Y velocity in NED frame in m/s
		    0, # Z velocity in NED frame in m/s
		    0, 0, 0, # afx, afy, afz acceleration (not supported yet)
		    0, 0)    # yaw, yaw_rate (not supported yet)
	
		# send command to vehicle
		self.pixhawk.send_mavlink(msg)
		self.pixhawk.flush()

	def manual_control_y(self,y):

		""" -----------------------------------------
		Control the drone in position according the y axis
		Param : y => distance (meters) 
		Return : /
			-----------------------------------------
		"""

		msg = self.pixhawk.message_factory.set_position_target_local_ned_encode(
		    0,       # time_boot_ms (not used)
		    0, 0,    # target system, target component
		    mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
		    0b0000111111111000, # type_mask (only position enabled)
		    0, # X Position 
		    float(y), # Y Position
		    0, # Altitude in meters 
		    0, # X velocity in NED frame in m/s
		    0, # Y velocity in NED frame in m/s
		    0, # Z velocity in NED frame in m/s
		    0, 0, 0, # afx, afy, afz acceleration (not supported yet)
		    0, 0)    # yaw, yaw_rate (not supported yet)
	
		# send command to vehicle
		self.pixhawk.send_mavlink(msg)
		self.pixhawk.flush()


	def send_global_velocity(self,velocity_x, velocity_y, velocity_z, duration):
		""" -----------------------------------------
		Control the drone in velocity according 3 axis
		Param : velocity_x => velocity (m/s) for x axis
				velocity_y => velocity (m/s) for y axis
				velocity_z => velocity (m/s) for z axis
				duration => time (s) where the drone change velocity
		Return : /
			-----------------------------------------
		"""
		

		msg = self.pixhawk.message_factory.set_position_target_global_int_encode(
		    0,       # time_boot_ms (not used)
		    0, 0,    # target system, target component
		    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
		    0b0000111111000111, # type_mask (only speeds enabled)
		    0, # X Position in WGS84 frame in 1e7 * meters
		    0, # Y Position in WGS84 frame in 1e7 * meters
		    0, # Altitude in meters
		    float(velocity_x), # X velocity in NED frame in m/s
		    float(velocity_y), # Y velocity in NED frame in m/s
		    float(velocity_z), # Z velocity in NED frame in m/s
		    0, 0, 0, # afx, afy, afz acceleration (not supported yet)
		    0, 0)    # yaw, yaw_rate (not supported yet) 

		# send command to vehicle on 1 Hz cycle
		for x in range(0,int(duration)):
		    self.pixhawk.send_mavlink(msg)
		    sleep(1)


	def condition_yaw(self,yaw):
		""" -----------------------------------------
			Change the yaw of the drone
			Param : yaw => angle to reach (degrees) 
			Return : /
			-----------------------------------------
		"""
		msg = self.pixhawk.message_factory.command_long_encode(
		    0, 0,    # target system, target component
		    mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
		    0, #confirmation
		    float(yaw), # param 1, yaw in degrees
		    0,          # param 2, yaw speed deg/s
		    1,          # param 3, direction -1 counter clockwise, 1 clockwise
		    0, 			# param 4, relative offset 1, absolute angle 0
		    0, 0, 0)    # param 5-7 not used

		# send command to vehicle
		self.pixhawk.send_mavlink(msg)


	"""------------------AUTONOM CONTROL--------------------"""

	def mission(self,file):
		""" -----------------------------------------
			The drone execute a mission autonomously from a file ".txt" 
			Param : file ".txt" to decode 
			Return : /
			-----------------------------------------
		"""

		print("Let's execute mission")
		lat=[]
		lon=[]
		alt=[]

		cmds=self.pixhawk.commands
		cmds.clear()
		

		with open(file) as f:
			for i, line in enumerate(f):
				buf=line.split(' ')
				if buf[0]=="Takeoff":
					cmd=Command(0,0,0,3,22,0,0,0,0,0,0,0,0,float(buf[3]))
				elif buf[0]=="Speed":
					cmd=Command(0,0,0,3,178,0,0,0,float(buf[3]),-1,0,0,0,10)
				elif buf[0]=="Location":
					cmd=Command(0,0,0,3,16,0,0,0,0,0,0,float(buf[2]),float(buf[3]),float(buf[4]))
					lat.append(float(buf[2]))
					lon.append(float(buf[3]))
					alt.append(float(buf[4]))
				elif buf[0]=="End":
					if buf[1]== "RTL":
						cmd=Command(0,0,0,3,20,0,0,0,0,0,0,0,0,0)
					elif buf[1]=="LAND":
						cmd=Command(0,0,0,3,21,0,0,0,0,0,0,0,0,0)
				else:
					break
				cmds.add(cmd)
																							
		cmds.upload()

		self.takeoff(10)
		self.pixhawk.commands.next=0
		self.mode("AUTO")
		while True:
			waypoint=self.pixhawk.commands.next
			print("Current Waypoint: %s",waypoint)
			if waypoint>1 and waypoint<cmds.count:
				d=self.calc_distance(self.current_location(),LocationGlobalRelative(lat[waypoint-2],lon[waypoint-2],alt[waypoint-2]))
				while d>10:
					d=self.calc_distance(self.current_location(),LocationGlobalRelative(lat[waypoint-2],lon[waypoint-2],alt[waypoint-2]))	
					print("Distance : " + str(d) + " meters")
					 
					sleep(1)

			if waypoint==cmds.count:
				break
			sleep(1)
					
if __name__=="__main__":
	print("Begin of the program")	

		

