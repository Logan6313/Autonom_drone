from dronekit import *
from pymavlink import mavutil
from time import sleep
import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

class Drone():

	def __init__(self):
		print("Creation of Drone instance")



if __name__=="__main__":
	print("Begin of the programm")

	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % args.connect
	vehicle = connect(args.connect, baud=115200, wait_ready=True)
	print("INITIALIZATION FINISHED")
	
	drone=Drone()
		

