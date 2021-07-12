#!/usr/bin/python


import sys
import socket
from PyQt4 import QtCore, QtGui, QtNetwork
import GUI

class Window(QtGui.QMainWindow,GUI.Ui_MainWindow):  
	def __init__(self,parent=None):

		super(Window, self).__init__(parent)  
		self.setupUi(self)
		self.Button_Send.clicked.connect(self.button)
		self.Button_Socket.clicked.connect(self.close_socket)
		self.comboBox_Command.currentIndexChanged.connect(self.list_event)
		self.horizontalSlider_Mode.sliderReleased.connect(self.slider_command)
		self.horizontalSlider_Mode.valueChanged.connect(self.slider_move)
		self.radioButton_Arm.clicked.connect(self.arm_on)
		self.radioButton_Disarm.clicked.connect(self.arm_off)
		self.Button_Mission.clicked.connect(self.mission)
		self.Button_Isarmable.clicked.connect(self.is_armable)


	def list_event(self):
		""" -----------------------------------------
		When the user press an item, the user can enter parameters according the command 
		Param : /
		Return : /
			-----------------------------------------
		"""
		print("Item pressed")
		self.clear()
		rank=self.comboBox_Command.currentIndex()
		print(rank)
		command=self.comboBox_Command.currentText()
		print(str(command))

		if rank==3:
			self.label_Param1.setText("Lat (degree)")
			self.label_Param2.setText("Lon (degree)")
			self.label_Param3.setText("Alt (m)")
			self.label_Parameter.setText("3 parameters :")

		elif rank==5 or rank==6:
			self.label_Param1.setText("Altitude (m)")
			self.label_Parameter.setText("1 parameter :")

		elif rank==7 or rank==8:
			self.label_Param1.setText("Distance (m)")
			self.label_Parameter.setText("1 parameter :")

		elif rank==9:
			self.label_Param1.setText("Yaw (degree)")
			self.label_Parameter.setText("1 parameter :")

		elif rank==10:
			self.label_Param1.setText("Airspeed (m/s)")
			self.label_Parameter.setText("1 parameter :")

		elif rank==11:
			self.label_Param1.setText("Vel_x (m/s)")
			self.label_Param2.setText("Vel_y (m/s)")
			self.label_Param3.setText("Vel_z (m/s)")
			self.label_Param4.setText("Duration (s)")
			self.label_Parameter.setText("4 parameters :")

		elif rank==12:
			self.label_Param1.setText("Lat (degree)")
			self.label_Param2.setText("Lon (degree)")
			self.label_Param3.setText("Alt (m)")
			self.label_Param4.setText("Airspeed (m/s)")
			self.label_Parameter.setText("4 parameters :")

		else:
			self.label_Parameter.setText("0 parameter")


	def slider_move(self):
		""" -----------------------------------------
		When the slider value changes, the label displays the different possibilities of flight mode
		Param : /
		Return : /
			-----------------------------------------
		"""

		print("Value slider changed")
		rank=self.horizontalSlider_Mode.sliderPosition()
		if rank==1:
			self.label_ModeBrowser.setText("GUIDED")
		elif rank==2:
			self.label_ModeBrowser.setText("AUTO")
		elif rank==3:
			self.label_ModeBrowser.setText("LAND")
		elif rank==4:
			self.label_ModeBrowser.setText("RTL")
		else:
			self.label_ModeBrowser.setText("STABILIZE")


	def slider_command(self):
		""" -----------------------------------------
		When the user releases the slider, a command to change flight mode is sent
		Param : /
		Return : /
			-----------------------------------------
		"""

		print("Value slider command")
		mes=str("mode" + " " + self.label_ModeBrowser.text())
		self.socket(str(mes))



	def button(self):
		""" -----------------------------------------
		When the user press the button "send", a specific command is sent 
		Param : /
		Return : /
			-----------------------------------------
		"""

		print("Button send pressed")

		if self.comboBox_Command.currentIndex()<3 or self.comboBox_Command.currentIndex()==4 :
			mes=str(self.comboBox_Command.currentText())

		elif self.comboBox_Command.currentIndex()==3:
			mes=str(self.comboBox_Command.currentText() + " " + self.lineEdit_Param1.text()+ " " + self.lineEdit_Param2.text()+ " " + self.lineEdit_Param3.text())
			
		elif self.comboBox_Command.currentIndex()>4 and self.comboBox_Command.currentIndex()<11:
			mes=str(self.comboBox_Command.currentText() + " " + self.lineEdit_Param1.text())
			
		else:
			mes=str(self.comboBox_Command.currentText() + " " + self.lineEdit_Param1.text()+ " " + self.lineEdit_Param2.text()+ " " + self.lineEdit_Param3.text()+ " " + self.lineEdit_Param4.text())
			

		self.socket(mes)
		self.clear()

	def is_armable(self):
		""" -----------------------------------------
		When the user press the button "is_armable?", a specific command to know if the vehicle is armable is sent
		Param : /
		Return : /
			-----------------------------------------
		"""
		mes="is_armable"
		self.socket(mes)

	def arm_on(self):
		""" -----------------------------------------
		When the user press the radiobutton "Arm", a specific command to arm the vehicle is sent
		Param : /
		Return : /
			-----------------------------------------
		"""
		print("Arm on checked")
		mes="arm on"
		self.socket(mes)
	

	def arm_off(self):
		""" -----------------------------------------
		When the user press the radiobutton "Disarm", a specific command to disarm the vehicle is sent
		Param : /
		Return : /
			-----------------------------------------
		"""

		print("Arm off checked")
		mes="arm off"
		self.socket(mes)
	
	def mission(self):
		""" -----------------------------------------
		When the user press the button "mission", a specific command to launch a mission is sent
		Param : /
		Return : /
			-----------------------------------------
		"""

		self.socket("mission")

	def close_socket(self):
		""" -----------------------------------------
		When the user press the button "Close socket", a specific command to close the socket is sent
		Param : /
		Return : /
			-----------------------------------------
		"""
		print("Button close socket pressed")
		self.socket("close")

	def socket(self,message):
		""" -----------------------------------------
		Send a message via the socket
		Param : message to send (string)
		Return : /
			-----------------------------------------
		"""
		print("Send message to the NVIDIA")
		enc_mes = message.encode()
		print('Sending "%s"' % message)
		sock.send(enc_mes)
		data=sock.recv(4096)
		print(data)
		self.textBrowser.setText(data)

	def clear(self):
		""" -----------------------------------------
		Method used to clear the different labels/editList 
		Param : /
		Return : /
			-----------------------------------------
		"""

		print("clear")
		self.label_Param1.clear()
		self.label_Param2.clear()
		self.label_Param3.clear()
		self.label_Param4.clear()
		self.lineEdit_Param1.clear()
		self.lineEdit_Param2.clear()
		self.lineEdit_Param3.clear() 
		self.lineEdit_Param4.clear()



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
