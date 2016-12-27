from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from MainWindow import Ui_MainWindow

class MainWindowTest(QMainWindow, Ui_MainWindow):
	"""docstring for MainWindowTest"""
	def __init__(self, parent=None):
		super(MainWindowTest, self).__init__(parent)
		self.parent = parent

		self.setupUi(self)
		self.setupButton()

	def setupButton(self):
		self.tablesHided = False
		self.hideButton.clicked.connect(self.showHide)
	# def setupUi(self):
	# 	# self.widget = QWidget(self)
	# 	# self.setCentralWidget(self.widget)
	# 	super().setupUi(self)
	# 	# self.widget.setLayout(self.gridLayout)

	def showHide(self):
		print ("showHide")
		if self.tablesHided is False:
			self.playlistTable.hide()
			self.songTable.hide()
			self.tablesHided = True
			self.resize((self.currentwidth), self.currentheight)
			self.resize((self.currentwidth - 100), self.currentheight)
		else:
			self.playlistTable.show()
			self.songTable.show()
			self.resize(self.currentwidth + 50, self.currentheight)
			self.tablesHided = False

	def resizeEvent(self, resizeEvent):
		self.currentwidth = resizeEvent.size().width()
		self.currentheight = resizeEvent.size().height()
		print ("The window has been resized - ", self.currentwidth, self.currentheight)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowTest()
    window.show()
    sys.exit(app.exec_())