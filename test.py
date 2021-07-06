#!/usr/bin/python


import sys
import socket
from PyQt4 import QtCore, QtGui, QtNetwork
import GUI
import time

class Window(QtGui.QMainWindow,GUI.Ui_MainWindow):  
	def __init__(self,parent=None):

		super(Window, self).__init__(parent)   #call the constructor QtGui.QWidget
		self.setupUi(self)
		
		self.pushButton.clicked.connect(self.button)
		self.pushButton_2.clicked.connect(self.erase)
		self.lineEdit.textChanged.connect(self.update)

	def button(self):
		print("Button1 pressed")
		self.lineEdit.setText("Karim")
		self.label.setText(self.lineEdit.displayText())

	def erase(self):
		print("Button2 pressed")
		self.lineEdit.clear()

	def update(self):
		self.label.setText(self.lineEdit.displayText())
		


if __name__ == "__main__":

	# Create a TCP/IP socket
	"""sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 
	# Connect the socket to the port where the server is listening
	server_address = ('192.168.1.86', 50010)
	print('Connecting to %s port %s' % server_address)
	sock.connect(server_address)"""
	app = QtGui.QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())
