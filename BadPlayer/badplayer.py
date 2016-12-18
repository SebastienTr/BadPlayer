import sys
from PyQt5.QtWidgets import (QMainWindow,
							 QTextEdit,
							 QAction,
							 QApplication,
							 QPushButton,
							 QLabel,
							 QHBoxLayout,
							 QVBoxLayout,
							 QWidget,
							 QGridLayout,
							 QLCDNumber,
							 QSlider)
from PyQt5.QtCore import (QCoreApplication,
						 Qt,
						 pyqtSignal,
						 QObject)
from PyQt5.QtGui import QIcon

from widgets import *


class BadPlayer(QMainWindow):
				
	def __init__(self):
		super().__init__()

		self.title = 'Bad Player'
		self.left = 100
		self.top = 100
		self.width = 640
		self.height = 480

		self.initUI()

	def initUI(self):

		# textEdit = QTextEdit()
		# self.setCentralWidget(textEdit)

		self.initMenu()
		# self.initGrid()

		# self.initSignals()

		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowTitle(self.title)
		self.show()

	def initMenu(self):
		print ("Init menu")

		mainMenu = self.menuBar() 
		fileMenu = mainMenu.addMenu('File')
		editMenu = mainMenu.addMenu('Edit')
		viewMenu = mainMenu.addMenu('View')
		searchMenu = mainMenu.addMenu('Search')
		toolsMenu = mainMenu.addMenu('Tools')
		helpMenu = mainMenu.addMenu('Help')

		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)
		fileMenu.addAction(exitButton)


def main():
	app = QApplication(sys.argv)
	ex = BadPlayer()
	sys.exit(app.exec_())
