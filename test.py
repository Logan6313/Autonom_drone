#!/usr/bin/python


import sys
import socket
from PyQt4 import QtCore, QtGui, QtNetwork
import GUI
import string

class Window(QtGui.QMainWindow,GUI.Ui_MainWindow):  
	def __init__(self,parent=None):

		super(Window, self).__init__(parent)   #call the constructor QtGui.QWidget
		self.setupUi(self)
		
		self.pushButton.clicked.connect(self.button)

	def button(self):
		print("Button1 pressed")
		mes="mode"
		enc_mes = mes.encode()
		print('Sending "%s"' % mes)
		sock.send(enc_mes)
		data=sock.recv(4096)
		print(data)
		self.lineEdit.setText(data)



if __name__ == "__main__":

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 
	# Connect the socket to the port where the server is listening
	server_address = ('192.168.1.86', 50010)
	print('Connecting to %s port %s' % server_address)
	sock.connect(server_address)

	app = QtGui.QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())
