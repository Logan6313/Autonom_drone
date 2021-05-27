from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import socket
from time import sleep

import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

def sock():
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		 
	# Bind the socket to the port
	server_address = ('192.168.1.86',50010)
	print ('starting up on %s port %s' % server_address)
	sock.bind(server_address)
		 
	# Listen for incoming connections
	sock.listen(1)

	# Wait for a connection
	print('Waiting for a connection')
	connection, client_address = sock.accept()
	print ('Connection from', client_address)

	data = connection.recv(1024)
	dec_data = data.decode()
	print('Received "%s"' % dec_data)
	if dec_data=="guided":
		guided()
	elif dec_data=="land":
		land()

	sleep(0.1)
	sock.close()


def guided():
	vehicle.mode = VehicleMode("GUIDED")
	sleep(1)
	print("Mode: %s" % vehicle.mode.name)

def land():
	vehicle.mode = VehicleMode("LAND")
	sleep(1)
	print("Mode: %s" % vehicle.mode.name)

if __name__ == "__main__":

	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % args.connect
	vehicle = connect(args.connect, baud=115200, wait_ready=True)
	print("INITIALIZATION FINISHED")
	print("Mode: %s" % vehicle.mode.name)

	sleep(5)

	sock()

	sleep(5)

	print ("Altitude relative to home_location: %s" % vehicle.location.global_relative_frame.alt)

	# Close vehicle object
	vehicle.close()
