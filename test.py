#!/usr/bin/python


import sys
from PyQt4 import QtCore, QtGui

class Window(QtGui.QWidget):  #Window class inherit from the QtGui.QWidget class 

	def __init__(self):

		super(Window, self).__init__()   #call the constructor QtGui.QWidget

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle("Interface")    
		
		button = QtGui.QPushButton('Click', self)
		button.resize(button.sizeHint())
		button.clicked.connect(self.button)

		self.show()

	def button(self):
		print("Button pressed")
	


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())


