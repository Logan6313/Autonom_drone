import socket

class SimpleSocket():

	def __init__(self,port=50010,address='192.168.1.86'):
		print("Creation of SimpleSocket instance")

		#Create a TCP/IP socket
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		#Bind the socket to the port
		server_address=(address,port)
		print ('starting up on %s port %s' % server_address)
		self.sock.bind(server_address)

		#Listen for incomimg connection
		self.sock.listen(1)
		#self.drone=drone
	
	
	#def __del__(self):
	#	print("Delete")

	def connect(self):
		#Wait for a connection
		print("Waiting for a connection")
		self.connection,client_address=self.sock.accept()

	def listener_loop(self):
		print("Start Listener")





if __name__=="__main__":
	print("Begin of the programm")
	Socket=SimpleSocket()
	Socket.connect()
	Socket.listener_loop()
