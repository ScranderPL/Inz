# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

import lib

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(538, 293)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.visualizeButton = QtWidgets.QPushButton(self.centralwidget)
		self.visualizeButton.setGeometry(QtCore.QRect(400, 130, 121, 121))
		self.visualizeButton.setObjectName("visualizeButton")
		self.visualizeButton.clicked.connect(self.visualize)
		
		self.generateButton = QtWidgets.QPushButton(self.centralwidget)
		self.generateButton.setGeometry(QtCore.QRect(400, 10, 121, 60))
		self.generateButton.setObjectName("generateButton")
		self.generateButton.clicked.connect(self.generate)
		
		self.generateLocalButton = QtWidgets.QPushButton(self.centralwidget)
		self.generateLocalButton.setGeometry(QtCore.QRect(400, 70, 121, 60))
		self.generateLocalButton.setObjectName("generateLocalButton")
		self.generateLocalButton.clicked.connect(self.generateLocal)


		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(10, 10, 351, 101))
		self.groupBox.setObjectName("groupBox")
		self.gpsButton = QtWidgets.QPushButton(self.groupBox)
		self.gpsButton.setGeometry(QtCore.QRect(180, 59, 141, 21))
		self.gpsButton.setObjectName("gpsButton")
		self.gpsButton.clicked.connect(self.openGPSFile)
		self.lidarButton = QtWidgets.QPushButton(self.groupBox)
		self.lidarButton.setGeometry(QtCore.QRect(180, 26, 141, 21))
		self.lidarButton.setObjectName("lidarButton")
		self.lidarButton.clicked.connect(self.openLiDARFile)
		self.lidarLabel = QtWidgets.QLabel(self.groupBox)
		self.lidarLabel.setGeometry(QtCore.QRect(22, 20, 161, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.lidarLabel.setFont(font)
		self.lidarLabel.setObjectName("lidarLabel")
		self.gpsLabel = QtWidgets.QLabel(self.groupBox)
		self.gpsLabel.setGeometry(QtCore.QRect(18, 58, 161, 20))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.gpsLabel.setFont(font)
		self.gpsLabel.setObjectName("gpsLabel")
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(10, 120, 371, 131))
		self.groupBox_2.setObjectName("groupBox_2")
		self.nameOfFileLabel = QtWidgets.QLabel(self.groupBox_2)
		self.nameOfFileLabel.setGeometry(QtCore.QRect(20, 20, 121, 31))
		self.nameOfFileLabel.setObjectName("nameOfFileLabel")
		self.xyzButton = QtWidgets.QPushButton(self.groupBox_2)
		self.xyzButton.setGeometry(QtCore.QRect(10, 60, 171, 61))
		self.xyzButton.setObjectName("xyzButton")
		self.xyzButton.clicked.connect(self.writeToXYZ)
		self.lasButton = QtWidgets.QPushButton(self.groupBox_2)
		self.lasButton.setGeometry(QtCore.QRect(190, 60, 171, 61))
		self.lasButton.setObjectName("lasButton")
		self.lasButton.clicked.connect(self.writeToLAS)
		
		self.nameOfFileTextEdit = QtWidgets.QTextEdit(self.groupBox_2)
		self.nameOfFileTextEdit.setGeometry(QtCore.QRect(150, 20, 211-60, 31))
		self.nameOfFileTextEdit.setObjectName("nameOfFileTextEdit")
		
		self.las2Button = QtWidgets.QPushButton(self.groupBox_2)
		self.las2Button.setGeometry(QtCore.QRect(300, 20, 60, 31))
		self.las2Button.setObjectName("lasButton")
		self.las2Button.clicked.connect(self.openWriteFile)
		
		self.groupBox_2.raise_()
		self.groupBox.raise_()
		self.visualizeButton.raise_()
		self.generateButton.raise_()
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 538, 21))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.actionWyjd_z_programu = QtWidgets.QAction(MainWindow)
		self.actionWyjd_z_programu.setObjectName("actionWyjd_z_programu")
		self.actionWyjd_z_programu.triggered.connect(self.close)
		self.menuFile.addAction(self.actionWyjd_z_programu)
		self.menubar.addAction(self.menuFile.menuAction())
		
		self.lidarFile = ""
		self.missionFile = ""

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Konwerter chmury punktów"))
		self.visualizeButton.setText(_translate("MainWindow", "Wizualizacja danych"))
		self.generateButton.setText(_translate("MainWindow", "Generacja chmury\n"
"(lat, lon)"))
		self.generateLocalButton.setText(_translate("MainWindow", "Generacja chmury\n"
"(x,y,z)"))
		self.groupBox.setTitle(_translate("MainWindow", "Dane wejściowe"))
		self.gpsButton.setText(_translate("MainWindow", "Wybierz plik"))
		self.lidarButton.setText(_translate("MainWindow", "Wybierz plik"))
		self.lidarLabel.setText(_translate("MainWindow", "Dane systemu LiDAR:"))
		self.gpsLabel.setText(_translate("MainWindow", "Log z Mission Planner:"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Dane wyjściowe"))
		self.nameOfFileLabel.setText(_translate("MainWindow", "Nazwa pliku wyjściowego \n"
"(bez rozszerzenia):"))
		self.xyzButton.setText(_translate("MainWindow", "Przekonwertuj dane \n"
" na format .xyz"))
		self.lasButton.setText(_translate("MainWindow", "Przekonwertuj dane \n"
" na format .las"))
		self.las2Button.setText(_translate("MainWindow", "Przeglądaj"))
		self.menuFile.setTitle(_translate("MainWindow", "Plik"))
		self.actionWyjd_z_programu.setText(_translate("MainWindow", "Wyjdź z programu"))

	def openLiDARFile(self):
		options = QFileDialog.Options()
		self.lidarFile, _ = QFileDialog.getOpenFileName(self.centralwidget, "Wybierz log systemu LiDAR", "", "Lidar Log (*.csv);;All Files (*)", options=options)


	def openGPSFile(self):
		options = QFileDialog.Options()
		self.missionFile, _ = QFileDialog.getOpenFileName(self.centralwidget, "Wybierz log programu Mission Planner", "", "Mission Planner's Log (*.log);;All Files (*)", options=options)

	def openWriteFile(self):
		options = QFileDialog.Options()
		self.missionFile, _ = QFileDialog.getSaveFileName(self.centralwidget, "Wybierz log programu Mission Planner", "", "Mission Planner's Log (*.log);;All Files (*)", options=options)
		self.nameOfFileTextEdit.setText("fdsfdsf")



	def writeToXYZ(self):
		if self.nameOfFileTextEdit.toPlainText() == "":
			print("Podaj nazwę")
			return
		if hasattr(self, 'xs'):
			name = self.nameOfFileTextEdit.toPlainText()
			name = name + ".xyz"
			lib.writeToXyz(name, self.xs, self.ys, self.zs)
		else:
			print("Proszę wygenerować chmurę punktów")
			return

	def writeToLAS(self):
		if self.nameOfFileTextEdit.toPlainText() == "":
			print("Podaj nazwę")
			return
		if hasattr(self, 'xs'):
			name = self.nameOfFileTextEdit.toPlainText()
			name = name + ".las"
			lib.writeToLas(name, self.xs, self.ys, self.zs)
		else:
			print("Proszę wygenerować chmurę punktów")
			return

	def visualize(self):
		if hasattr(self, 'xs'):
			lib.visualize(self.xs, self.ys, self.zs, self.genOption)
		else:
			print("Proszę wygenerować chmurę punktów")
		pass

	def generate(self):
		if self.lidarFile == "" or self.missionFile == "":
			print("Podaj pliki wejściowe")
			return
		else:
			print("Generacja z dwóch plików")
		self.xs, self.ys, self.zs = lib.generation(self.lidarFile, self.missionFile, "geo")
		self.genOption = "geo"
		
	def generateLocal(self):
		if self.lidarFile == "" or self.missionFile == "":
			print("Podaj pliki wejściowe")
			return
		else:
			print("Generacja z dwóch plików")
		self.xs, self.ys, self.zs = lib.generation(self.lidarFile, self.missionFile, "xyz")
		self.genOption = "xyz"


	def close(self):
		exit(0)
		


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
