from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import badwidgets as widgets
import badmodels as models

import logging
import yaml
import sys
import vlc
import os

class TestWindow(QMainWindow):
	"""docstring for TestWindow"""
	def __init__(self, parent):
		super(TestWindow, self).__init__()
		self.parent = parent

		self.initUI()
		
	def initUI(self):
		self.label = QtWidgets.QLabel('Yeah !', self)
		# self.label.setObjectName("label")
		self.setGeometry(200, 200, 200, 200)
		self.setWindowFlags(QWindow)
		# self.setCentralWidget(self.label)
		self.show()


class BadPlayer(QMainWindow):

	def __init__(self, config):
		super().__init__()

		self.title = 'Bad Player'
		self.left = 100
		self.top = 100
		self.width = 600
		self.height = 480
		self.isPaused = False

		self.config = config
		self.clickedPL = None
		self.clickedSong = None

		self.playlistpath = os.path.realpath(os.path.dirname(os.path.realpath("{}/../".format(__file__))) + '/' + config['browser']['playlistpath'])
		os.makedirs(self.playlistpath, exist_ok=True)

		self.initVLC(self.config['player'])
		self.initDB(self.config['database'])
		self.initUI()

		# hiphop = self.session.query(models.Playlist).all()[1]
		# newsong = models.Song(name="My Hip Hop song !", localpath="02.mp3", source="File")
		# newsong.playlists.append(hiphop)
		# self.session.add(newsong)
		# self.session.commit()


	def initVLC(self, config):
		self.instance = vlc.Instance()
		self.mediaplayer = self.instance.media_player_new()
		self.mediaplayer.audio_set_volume(config['default_volume'])

		logging.getLogger("vlc").setLevel(logging.NOTSET)
		logging.getLogger("mpgatofixed32").setLevel(logging.NOTSET)		
		logging.getLogger("core vout").setLevel(logging.NOTSET)

	def initDB(self, config):
		self.session = models.createSession(config)

	def initUI(self):
		self.initPlayer()
		self.initMenu()

		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowTitle(self.title)
		self.show()

		self.setStatus("Ready")

	def initMenu(self):
		# Actions
		open = QAction("&Open", self)
		open.triggered.connect(self.OpenFile)
		addPlaylist = QAction("&Add playlist", self)
		addPlaylist.triggered.connect(self.addPlaylist)
		addSongFromFile = QAction("&Add song from file", self)
		addSongFromFile.triggered.connect(self.addSongFromFile)
		exit = QAction("&Exit", self)
		exit.triggered.connect(sys.exit)
		newWindow = QAction("&New window", self)
		newWindow.triggered.connect(self.newWindow)

		# Menubar
		menubar = self.menuBar()
		filemenu = menubar.addMenu("&File")
		filemenu.addAction(open)
		filemenu.addSeparator()
		filemenu.addAction(exit)
		filemenu.addAction(newWindow)
		playlistmenu = menubar.addMenu("&Playlists")
		playlistmenu.addAction(addPlaylist)
		songsmenu = menubar.addMenu("&Songs")
		songsmenu.addAction(addSongFromFile)
		searchMenu = menubar.addMenu("&Help")
		searchMenu.addAction(open)

	def initPlayer(self):
		"""Set up the user interface, signals & slots
		"""
		self.widget = QWidget(self)
		self.setCentralWidget(self.widget)
		self.getIcons()

		self.initVideoFrame()
		test = Qt.Key_MediaPlay

		# Position slider
		self.positionslider = QSlider(Qt.Horizontal, self)
		self.positionslider.setToolTip("Position")
		self.positionslider.setMaximum(1000)
		self.positionslider.sliderMoved.connect(self.setPosition)
		self.positionslider.valueChanged.connect(self.valueChanged)
		self.positionslider.sliderPressed.connect(self.sliderPressed)
		self.positionvalue = 0

		# Buttons
		self.hbuttonbox = QHBoxLayout()
		self.playbutton = self.getButton(funct=self.PlayPause, icon=self.playicon)
		self.hbuttonbox.addWidget(self.playbutton)
		self.stopbutton = self.getButton(funct=self.Stop, icon=self.stopicon)
		self.hbuttonbox.addWidget(self.stopbutton)

		# Volume slider
		self.hbuttonbox.addStretch(1)

		self.volumeslider = QSlider(Qt.Horizontal, self)
		self.volumeslider.setToolTip("Volume")
		self.volumeslider.setMaximum(100)
		self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
		self.hbuttonbox.addWidget(self.volumeslider)
		self.volumeslider.valueChanged.connect(self.setVolume)

		self.showHideButton = self.getButton(funct=self.ShowHide, text="show", style=False)
		# self.fullscreenbutton = self.getButton(funct=self.FullScreen, text="FullScreen", style=False)
		# self.hbuttonbox.addWidget(self.fullscreenbutton)
		self.hbuttonbox.addWidget(self.showHideButton)

		self.vplayerlayout = QVBoxLayout()
		self.vplayerlayout.addWidget(self.videoframe)
		self.vplayerlayout.addWidget(self.positionslider)
		self.vplayerlayout.addLayout(self.hbuttonbox)

		self.initLists()

		self.mainlayout = QHBoxLayout()
		self.mainlayout.addLayout(self.vplayerlayout)
		self.mainlayout.addLayout(self.listslayout)

		self.widget.setLayout(self.mainlayout)

		self.timer = QTimer(self)
		self.timer.setInterval(200)
		self.timer.timeout.connect(self.updateUI)

	def initVideoFrame(self):
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

	def initLists(self):
		self.listslayout = QHBoxLayout()

		self.songsqlist = widgets.SongsWidget(self, models.Song)
		self.playlistsqlist = widgets.PlaylistsWidget(self, models.Playlist, self.songsqlist)

		self.listslayout.addWidget(self.playlistsqlist)
		self.listslayout.addWidget(self.songsqlist)
		self.qlistsIsHided = False
		self.width += 600

	def newWindow(self):
		print ("New window ...")
		nw = TestWindow(self)
		nw.show()



	def valueChanged(self, t):
		self.positionvalue = t

	def getButton(self, funct=None, icon=None, text=None, style=True):
		if text is not None:
			button = QPushButton(text)
		else:
			button = QPushButton()
		if funct is not None:
			button.clicked.connect(funct)
		if icon is not None:
			button.setIcon(icon)
			button.setIconSize(QSize(50, 50))
		if style is True:
			button.setFlat(True)
			button.setStyleSheet("color: black; background-color: black")

		return button

	def FullScreen(self):
		print ('fs')

	def ShowHide(self):
		# print (self.geometry().width(), self.geometry().height())

		# print (locals())

		if self.qlistsIsHided is False:
			self.playlistsqlist.hide()
			self.songsqlist.hide()
			# self.resize((self.width), self.height)
			self.resize(self.vplayerlayout.geometry().width() + 23, self.geometry().height())
			self.qlistsIsHided = True
		else:
			# self.resize((self.width + PWidth + SWidth + 200), self.height)
			self.playlistsqlist.show()
			self.songsqlist.show()
			# self.playlistsqlist.resize(30, self.playlistsqlist.geometry().height())
			# self.songsqlist.resize(30, self.songsqlist.geometry().height())
			self.resize((self.geometry().width() + self.listslayout.geometry().width() + 281), self.geometry().height())
			# self.resize((self.width + 590), self.geometry().height())
			self.qlistsIsHided = False

	def resizeEvent(self, resizeEvent):
		# print ("The window has been resized - ", resizeEvent.size())
		pass


	def getIcons(self):
		self.playicon = self.getImage('player', 'play.png')
		self.pauseicon = self.getImage('player', 'pause.png')
		self.stopicon = self.getImage('player', 'stop.png')

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

	def addSongFromFile(self):
		dialog = widgets.AddSongDialog(self)
		ok, filename, playlistname, playlistid = dialog.get()
		# print ("Ok :", ok)
		# print ("filename :", filename)
		# print ("playlistname :", playlistname)
		# print ("playlistid :", playlistid)
		# print ("self.playlistpath :", self.playlistpath)
		if ok:
			models.add_song(self.session, filename, playlistname, playlistid, self.playlistpath)

	def addPlaylist(self):
		dialog = widgets.AddPlaylistDialog(self)
		ok = dialog.showDialog()
		if ok:
			name = dialog.getText()
			path = self.playlistpath + '/' + name
			newPlaylist = models.Playlist(name=name)
			os.makedirs(self.playlistpath + '/' + name, exist_ok=True)
			self.session.add(newPlaylist)
			self.session.commit()
			self.playlistsqlist.refresh()
			self.setStatus('Playlist added')
		else:
			self.setStatus('Operation cancelled')


	def OpenFile(self, filename=None):
		"""Open a media file in a MediaPlayer
		"""
		filename=None
		if filename is None:
			filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))[0]
		if not filename:
			return

		if sys.version < '3': 
			filename = unicode(filename)

		self.setFile(filename)

	def setFile(self, filename):
		self.media = self.instance.media_new(filename)
		self.mediaplayer.set_media(self.media)
		self.media.parse()
		self.setWindowTitle(self.media.get_meta(0))

		if sys.platform.startswith('linux'): # for Linux using the X Server
			self.mediaplayer.set_xwindow(self.videoframe.winId())
		elif sys.platform == "win32": # for Windows
			self.mediaplayer.set_hwnd(self.videoframe.winId())
		elif sys.platform == "darwin": # for MacOS
			self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
		self.PlayPause()
		self.setStatus("Media added to player")

	def setVolume(self, Volume):
		"""Set the volume
		"""
		self.mediaplayer.audio_set_volume(Volume)

	def setPosition(self, position):
		"""Set the position
		"""
		# setting the position to where the slider was dragged
		self.mediaplayer.set_position(position / 1000.0)

	def updateUI(self):
		"""updates the user interface"""
		# setting the slider to the desired position
		self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

		if not self.mediaplayer.is_playing():
			# no need to call this function if nothing is played
			self.timer.stop()
			if not self.isPaused:
				self.Stop()

	def setStatus(self, message):
		if message is None:
			self.statusBar().hide()
		else:
			self.statusBar().showMessage(message)

	## Need play/pause for the Space key event
	def keyPressEvent(self, e):
		# print ("Key press event : ", e.text())
		self.statusBar().showMessage(e.text() + ' key was pressed')
		if e.key() == Qt.Key_Escape:
			self.close()

def loadConfig():
	config = None
	# print ('###########', "{}/config.yml".format(os.path.realpath(os.path.dirname(__file__))))
	configpath = "{}/config.yml".format(os.path.realpath(os.path.dirname(__file__)))
	with open(configpath, 'r') as stream:
		try:
			config = yaml.load(stream)
		except yaml.YAMLError as exc:
			print ("Wrong config file ./config.yml" + str(exc))
			os._exit(1)
	return config

def main():
	app = QApplication(sys.argv)
	config = loadConfig()
	ex = BadPlayer(config)
	sys.exit(app.exec_())

