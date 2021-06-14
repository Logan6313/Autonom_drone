from dronekit import *
from pymavlink import mavutil
from time import sleep
import math


class Drone():

	def __init__(self,pixhawk):
		print("Creation of Drone instance")
		self.pixhawk=pixhawk
	
	def info(self):
			vehicle_state=[self.pixhawk.version,self.pixhawk.location.global_frame.lat,self.pixhawk.location.global_frame.lon,
self.pixhawk.location.global_frame.alt,self.pixhawk.attitude.yaw,self.pixhawk.battery.voltage,self.pixhawk.battery.level]

			return vehicle_state

	def set_mode(self,data=None):
		print("Change flight mode")
		if data is None:
			return self.pixhawk.mode
		else:
			self.pixhawk.mode=VehicleMode(data)

	def arm(self,state=None):

		if state is None:
			return self.pixhawk.armed

		elif state=="on":
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

			return True

		elif state=="off":
			print("Let's disarm !")
			self.pixhawk.armed=False
			while not self.pixhawk.armed==False:
				print " Waiting for disarming..."
				time.sleep(1)

			return True


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

		self.arm("on")
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

	def calc_distance(self,current,target):
		c_lat=math.radians(current.lat)
		t_lat=math.radians(target.lat)
		c_lon=math.radians(current.lon)
		t_lon=math.radians(target.lon)

		d=6371*math.acos(math.sin(c_lat)*math.sin(t_lat)+math.cos(c_lat)*math.cos(t_lat)*math.cos(t_lon-c_lon))
		
		return d*1000


	def mission(self,file):
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
		self.set_mode("AUTO")
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

	def manual_control_x(self,x):
		msg=self.pixhawk.message_factory.set_position_target_local_ned_encode(0,0,0,8,0b0000111111000000,float(x),0,0,0,0,0,0,0,0,0,0)
		self.pixhawk.send_mavlink(msg)
		self.pixhawk.flush()

	def manual_control_y(self,y):
		msg=self.pixhawk.message_factory.set_position_target_local_ned_encode(0,0,0,8,0b0000111111000000,0,float(y),0,0,0,0,0,0,0,0,0)
		self.pixhawk.send_mavlink(msg)
		self.pixhawk.flush()

	def send_global_velocity(velocity_x, velocity_y, velocity_z, duration):

		msg = self.pixhawk.message_factory.set_position_target_global_int_encode(
		    0,       # time_boot_ms (not used)
		    0, 0,    # target system, target component
		    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
		    0b0000111111000111, # type_mask (only speeds enabled)
		    0, # lat_int - X Position in WGS84 frame in 1e7 * meters
		    0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
		    0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
		    # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
		    float(velocity_x), # X velocity in NED frame in m/s
		    float(velocity_y), # Y velocity in NED frame in m/s
		    float(velocity_z), # Z velocity in NED frame in m/s
		    0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
		    0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

		# send command to vehicle on 1 Hz cycle
		for x in range(0,int(duration)):
		    self.pixhawk.send_mavlink(msg)
		    sleep(1)


	def condition_yaw(self,yaw):

		# create the CONDITION_YAW command using command_long_encode()
		msg = self.pixhawk.message_factory.command_long_encode(
		    0, 0,    # target system, target component
		    mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
		    0, #confirmation
		    float(yaw),    # param 1, yaw in degrees
		    0,          # param 2, yaw speed deg/s
		    1,          # param 3, direction -1 ccw, 1 cw
		    0, # param 4, relative offset 1, absolute angle 0
		    0, 0, 0)    # param 5 ~ 7 not used
		# send command to vehicle
		self.pixhawk.send_mavlink(msg)


		
					
if __name__=="__main__":
	print("Begin of the program")	

		

