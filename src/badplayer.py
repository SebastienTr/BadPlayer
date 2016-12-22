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
							 QSlider,
							 QFileDialog,
							 QFrame,
							 QSplitter,
							 QStyleFactory,
							 QListWidget,
							 QListWidgetItem)
from PyQt5.QtCore import (QCoreApplication,
						 Qt,
						 pyqtSignal,
						 QObject,
						 QTimer,
						 QSize)
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap

from badwidgets import *

import vlc

import os

import logging


class BadPlayer(QMainWindow):
				
	def __init__(self):
		super().__init__()

		self.title = 'Bad Player'
		self.left = 100
		self.top = 100
		self.width = 1000
		self.height = 480

		self.instance = vlc.Instance()
		self.mediaplayer = self.instance.media_player_new()

		logging.getLogger("vlc").setLevel(logging.NOTSET)
		logging.getLogger("core").setLevel(logging.NOTSET)

		self.initUI()
		self.isPaused = False

	def initUI(self):

		# textEdit = QTextEdit()
		# self.setCentralWidget(textEdit)

		# self.initMenu()
		self.initPlayer()
		# self.initGrid()

		# self.initSignals()

		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowTitle(self.title)
		self.show()

	def initMenu(self):
		print ("Init menu")
		self.mainMenu = self.menuBar() 
		self.mainMenu.setNativeMenuBar(False)
		fileMenu = self.mainMenu.addMenu('File')
		editMenu = self.mainMenu.addMenu('Edit')
		viewMenu = self.mainMenu.addMenu('View')
		searchMenu = self.mainMenu.addMenu('Search')
		toolsMenu = self.mainMenu.addMenu('Tools')
		helpMenu = self.mainMenu.addMenu('Help')

		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)
		fileMenu.addAction(exitButton)

	def initPlayer(self):
		"""Set up the user interface, signals & slots
		"""
		self.widget = QWidget(self)
		self.setCentralWidget(self.widget)

		# In this widget, the video will be drawn
		if sys.platform == "darwin": # for MacOS
			from PyQt5.QtWidgets import QMacCocoaViewContainer	
			self.videoframe = QMacCocoaViewContainer(0)
		else:
			self.videoframe = QFrame()
		self.palette = self.videoframe.palette()
		self.palette.setColor (QPalette.Window,
							   QColor(0,0,0))
		self.videoframe.setPalette(self.palette)
		self.videoframe.setAutoFillBackground(True)

		self.positionslider = QSlider(Qt.Horizontal, self)
		self.positionslider.setToolTip("Position")
		self.positionslider.setMaximum(1000)
		self.positionslider.sliderMoved.connect(self.setPosition)
		self.positionslider.valueChanged.connect(self.valueChanged)
		self.positionslider.sliderPressed.connect(self.sliderPressed)
		self.positionvalue = 0

		self.hbuttonbox = QHBoxLayout()
		self.playicon = self.getImage('player', 'play.png')
		self.pauseicon = self.getImage('player', 'pause.png')
		self.playbutton = QPushButton()
		self.playbutton.clicked.connect(self.PlayPause)
		self.playbutton.setIcon(self.playicon)
		self.playbutton.setIconSize(QSize(50, 50))
		self.playbutton.setFlat(True)
		self.hbuttonbox.addWidget(self.playbutton)

		self.stopbutton = QPushButton()
		self.stopicon = self.getImage('player', 'stop.png')
		self.stopbutton.setIcon(self.stopicon)
		self.stopbutton.setIconSize(QSize(50, 50))
		self.stopbutton.setFlat(True)
		self.hbuttonbox.addWidget(self.stopbutton)
		self.stopbutton.clicked.connect(self.Stop)

		self.hbuttonbox.addStretch(1)
		self.volumeslider = QSlider(Qt.Horizontal, self)
		self.volumeslider.setMaximum(100)
		self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
		self.volumeslider.setToolTip("Volume")
		self.hbuttonbox.addWidget(self.volumeslider)
		self.volumeslider.valueChanged.connect(self.setVolume)

		self.vplayerlayout = QVBoxLayout()
		self.vplayerlayout.addWidget(self.videoframe)
		self.vplayerlayout.addWidget(self.positionslider)
		self.vplayerlayout.addLayout(self.hbuttonbox)


		self.listslayout = QHBoxLayout()

		self.playlistsqlist = QListWidget()
		items = ('Jazz', 'Rock', 'Hip Hop')
		for i, item in enumerate(items):
			qitem = QListWidgetItem(item)
			self.playlistsqlist.insertItem(i, qitem)

		self.songsqlist = QListWidget()
		self.songsqlist.width = 100
		items = ('One song', 'Another', 'And another again')
		for i, item in enumerate(items):
			qitem = QListWidgetItem(item)
			self.songsqlist.insertItem(i, qitem)

		self.listslayout.addWidget(self.playlistsqlist)
		self.listslayout.addWidget(self.songsqlist)


		self.mainlayout = QHBoxLayout()
		self.mainlayout.addLayout(self.vplayerlayout)
		self.mainlayout.addLayout(self.listslayout)



		self.widget.setLayout(self.mainlayout)

		open = QAction("&Open", self)
		open.triggered.connect(self.OpenFile)
		exit = QAction("&Exit", self)
		exit.triggered.connect(sys.exit)
		menubar = self.menuBar()
		filemenu = menubar.addMenu("&File")
		filemenu.addAction(open)
		filemenu.addSeparator()
		filemenu.addAction(exit)

		self.timer = QTimer(self)
		self.timer.setInterval(200)
		self.timer.timeout.connect(self.updateUI)

	def valueChanged(self, t):
		self.positionvalue = t

	def sliderPressed(self, t=-1):
		self.mediaplayer.set_position(self.positionvalue / 1000.0)

	def getImage(self, folder, filename):
		icon = QIcon(QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/images/{}/{}'.format(folder,filename)))
		return icon

	def PlayPause(self):
		"""Toggle play/pause status
		"""
		if self.mediaplayer.is_playing():
			self.mediaplayer.pause()
			self.playbutton.setIcon(self.playicon)
			self.isPaused = True
		else:
			if self.mediaplayer.play() == -1:
				self.OpenFile()
				return
			self.mediaplayer.play()
			self.playbutton.setIcon(self.pauseicon)
			self.timer.start()
			self.isPaused = False

	def Stop(self):
		"""Stop player
		"""
		self.mediaplayer.stop()
		self.playbutton.setIcon(self.playicon)

	def OpenFile(self, filename=None):
		"""Open a media file in a MediaPlayer
		"""
		if filename is None:
			filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))[0]
		if not filename:
			return

		# create the media
		if sys.version < '3':
			filename = unicode(filename)
		self.media = self.instance.media_new(filename)
		# put the media in the media player
		self.mediaplayer.set_media(self.media)

		# parse the metadata of the file
		self.media.parse()
		# set the title of the track as window title
		self.setWindowTitle(self.media.get_meta(0))

		# the media player has to be 'connected' to the QFrame
		# (otherwise a video would be displayed in it's own window)
		# this is platform specific!
		# you have to give the id of the QFrame (or similar object) to
		# vlc, different platforms have different functions for this
		if sys.platform.startswith('linux'): # for Linux using the X Server
			self.mediaplayer.set_xwindow(self.videoframe.winId())
		elif sys.platform == "win32": # for Windows
			self.mediaplayer.set_hwnd(self.videoframe.winId())
		elif sys.platform == "darwin": # for MacOS
			self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
		self.PlayPause()

	def setVolume(self, Volume):
		"""Set the volume
		"""
		self.mediaplayer.audio_set_volume(Volume)

	def setPosition(self, position):
		"""Set the position
		"""
		# setting the position to where the slider was dragged
		self.mediaplayer.set_position(position / 1000.0)
		# the vlc MediaPlayer needs a float value between 0 and 1, Qt
		# uses integer variables, so you need a factor; the higher the
		# factor, the more precise are the results
		# (1000 should be enough)

	def updateUI(self):
		"""updates the user interface"""
		# setting the slider to the desired position
		self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

		if not self.mediaplayer.is_playing():
			# no need to call this function if nothing is played
			self.timer.stop()
			if not self.isPaused:
				# after the video finished, the play button stills shows
				# "Pause", not the desired behavior of a media player
				# this will fix it
				self.Stop()


def main():
	app = QApplication(sys.argv)
	ex = BadPlayer()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
