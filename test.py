#!/usr/bin/python


import sys
import socket
from PyQt4 import QtCore, QtGui, QtNetwork
import GUI

class Window(QtGui.QMainWindow,GUI.Ui_MainWindow):  
	def __init__(self,parent=None):

		super(Window, self).__init__(parent)  
		self.setupUi(self)
		self.commandLinkButton.clicked.connect(self.button)
		self.pushButton_2.clicked.connect(self.close_socket)
		self.comboBox.currentIndexChanged.connect(self.list_event)
		self.horizontalSlider.sliderReleased.connect(self.slider_command)
		self.horizontalSlider.valueChanged.connect(self.slider_move)
		self.radioButton.clicked.connect(self.arm_on)
		self.radioButton_2.clicked.connect(self.arm_off)
		self.pushButton.clicked.connect(self.mission)


	def list_event(self):
		print("Item pressed")
		self.clear()
		rank=self.comboBox.currentIndex()
		print(rank)
		command=self.comboBox.currentText()
		print(str(command))

		if rank==3:
			self.label_2.setText("Lat (degree)")
			self.label_3.setText("Lon (degree)")
			self.label_4.setText("Alt (m)")
			self.label_11.setText("3 parameters :")

		elif rank==5 or rank==6:
			self.label_2.setText("Altitude (m)")
			self.label_11.setText("1 parameter :")

		elif rank==7 or rank==8:
			self.label_2.setText("Distance (m)")
			self.label_11.setText("1 parameter :")

		elif rank==9:
			self.label_2.setText("Yaw (degree)")
			self.label_11.setText("1 parameter :")

		elif rank==10:
			self.label_2.setText("Airspeed (m/s)")
			self.label_11.setText("1 parameter :")

		elif rank==11:
			self.label_2.setText("Vel_x (m/s)")
			self.label_3.setText("Vel_y (m/s)")
			self.label_4.setText("Vel_z (m/s)")
			self.label_5.setText("Duration (s)")
			self.label_11.setText("4 parameters :")

		elif rank==12:
			self.label_2.setText("Lat (degree)")
			self.label_3.setText("Lon (degree)")
			self.label_4.setText("Alt (m)")
			self.label_5.setText("Airspeed (m/s)")
			self.label_11.setText("4 parameters :")

		else:
			self.label_11.setText("0 parameter")

	def slider_command(self):
		print("Value slider command")
		mes=str("mode" + " " + self.label_6.text())
		self.socket(str(mes))

	def slider_move(self):
		print("Value slider changed")
		rank=self.horizontalSlider.sliderPosition()
		if rank==1:
			self.label_6.setText("GUIDED")
		elif rank==2:
			self.label_6.setText("AUTO")
		elif rank==3:
			self.label_6.setText("LAND")
		elif rank==4:
			self.label_6.setText("RTL")
		else:
			self.label_6.setText("STABILIZE")


	def button(self):
		print("Button pressed")

		if self.comboBox.currentIndex()<3 or self.comboBox.currentIndex()==4 :
			mes=str(self.comboBox.currentText())

		elif self.comboBox.currentIndex()==3:
			mes=str(self.comboBox.currentText() + " " + self.lineEdit_2.text()+ " " + self.lineEdit_3.text()+ " " + self.lineEdit_4.text())
			
		elif self.comboBox.currentIndex()>4 and self.comboBox.currentIndex()<11:
			mes=str(self.comboBox.currentText() + " " + self.lineEdit_2.text())
			
		else:
			mes=str(self.comboBox.currentText() + " " + self.lineEdit_2.text()+ " " + self.lineEdit_3.text()+ " " + self.lineEdit_4.text()+ " " + self.lineEdit_5.text())
			


		self.socket(mes)
		self.clear()

	def arm_on(self):
		print("Arm on checked")
		mes="arm on"
		self.socket(mes)
	

	def arm_off(self):
		print("Arm off checked")
		mes="arm off"
		self.socket(mes)
	
	def mission(self):
		self.socket("mission")

	def close_socket(self):
		print("Button pressed")
		self.socket("close")

	def socket(self,message):
		print("Send message to the NVIDIA")
		enc_mes = message.encode()
		print('Sending "%s"' % message)
		sock.send(enc_mes)
		data=sock.recv(4096)
		print(data)
		self.textBrowser.setText(data)

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

	"""# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 
	# Connect the socket to the port where the server is listening
	server_address = ('192.168.1.86', 50010)
	print('Connecting to %s port %s' % server_address)
	sock.connect(server_address)"""

	app = QtGui.QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())
