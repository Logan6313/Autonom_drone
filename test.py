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
		
		self.commandLinkButton.clicked.connect(self.button)
		self.comboBox.currentIndexChanged.connect(self.list_event)


	def list_event(self):
		print("Item pressed")
		rank=self.comboBox.currentIndex()
		print(rank)
		command=self.comboBox.currentText()
		print(str(command))

		if rank==3:
			self.label_2.setText("Altitude (m)")




	def button(self):
		print("Button pressed")
		if self.comboBox.currentIndex()<3:
			mes=str(self.comboBox.currentText())
		elif self.comboBox.currentIndex()==3:
			mes=str(self.comboBox.currentText() + " " + self.lineEdit_2.text())

		self.socket(str(mes))
		self.clear()

	def socket(self,message):
		print("Send message to the NVIDIA")
		enc_mes = message.encode()
		print('Sending "%s"' % message)
		sock.send(enc_mes)
		data=sock.recv(4096)
		print(data)
		self.lineEdit.setText(data)

	def clear(self):
		print("clear")
		self.label_2.clear()
		self.label_3.clear()
		self.label_4.clear()
		self.label_5.clear()
		self.lineEdit_2.clear()
		self.lineEdit_3.clear()
		self.lineEdit_4.clear() 
		self.lineEdit_5.clear()



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
