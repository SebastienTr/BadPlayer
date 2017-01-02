from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui.Downloader import Ui_Downloader

class Downloader(QMainWindow, Ui_Downloader):
	"""docstring for Downloader"""
	def __init__(self, parent):
		super(Downloader, self).__init__()
		self.parent = parent
		# self.downloader = QMa

		self.setupUi(self)
