# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(836, 637)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(560, 70, 261, 421))
        self.lineEdit.setText(_fromUtf8(""))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.commandLinkButton = QtGui.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(640, 510, 81, 41))
        self.commandLinkButton.setStyleSheet(_fromUtf8(""))
        self.commandLinkButton.setObjectName(_fromUtf8("commandLinkButton"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 400, 113, 23))
        self.lineEdit_2.setText(_fromUtf8(""))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 400, 113, 23))
        self.lineEdit_3.setText(_fromUtf8(""))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(270, 400, 113, 23))
        self.lineEdit_4.setText(_fromUtf8(""))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(400, 400, 113, 23))
        self.lineEdit_5.setText(_fromUtf8(""))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(220, 260, 79, 23))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 370, 61, 21))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 370, 51, 21))
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(300, 370, 71, 21))
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(170, 370, 61, 21))
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 20, 151, 31))
        self.label.setStyleSheet(_fromUtf8("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.495 rgba(255, 255, 255, 255), stop:0.505 rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255));"))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Interface", None))
        self.commandLinkButton.setText(_translate("MainWindow", "SEND", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "info", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "mode", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "arm", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "takeoff", None))
        self.label_2.setText(_translate("MainWindow", "Param1", None))
        self.label_3.setText(_translate("MainWindow", "Param4", None))
        self.label_4.setText(_translate("MainWindow", "Param3", None))
        self.label_5.setText(_translate("MainWindow", "Param2", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#000000;\">Command</span></p></body></html>", None))

