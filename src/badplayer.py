from PyQt5.QtGui import *
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

# from ui.MainWindow import Ui_MainWindow
from ui.MainWindow_test import Ui_MainWindow

# class BadPlayer(QMainWindow, Ui_MainWindow_test):
class BadPlayer(QMainWindow, Ui_MainWindow):
	"""docstring for BadPlayer"""
	def __init__(self, config):
		super(BadPlayer, self).__init__()
		self.title = 'Bad Player'
		# self.parent = parent

		self.config = config
		self.clickedPL = None
		self.clickedSong = None
		self.firstFillPL = True
		self.firstFillSG = True

		self.setupUi(self)

		self.playlistpath = os.path.realpath(os.path.dirname(os.path.realpath("{}/../".format(__file__))) + '/' + config['browser']['playlistpath'])
		os.makedirs(self.playlistpath, exist_ok=True)

		self.initVLC(self.config['player'])
		self.initDB(self.config['database'])
		self.initUI()
		self.initMenu()

		self.show()

		self.afterShow()

	def afterShow(self):
		# self.playlistTable.setColumnWidth(0, self.playlistTable.geometry().width())
		# self.songTable.setColumnWidth(0, self.songTable.geometry().width())
		pass

	def initUI(self):
		self.initButton()

		self.initTables()

		self.timer = QTimer(self)
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.updateUI)
		self.setWindowTitle(self.title)

	def initTables(self):
		self.currentPlaylist = None
		self.playlistTable.currentItemChanged.connect(self.playListChanged)
		self.fillPlaylistTable()
		self.playlistTable.setCurrentItem(self.qall)

		self.songTable.itemDoubleClicked.connect(self.musicDoubleClicked)


	def initMenu(self):
		self.actionOpen.triggered.connect(self.OpenFile)
		self.actionExit.triggered.connect(sys.exit)
		self.actionAddPlaylist.triggered.connect(self.addPlaylist)
		self.actionAddMusicFromFile.triggered.connect(self.addSongFromFile)

	def fillPlaylistTable(self):
		items = self.session.query(models.Playlist).all()

		self.playlistTable.setColumnCount(1)
		# self.playlistTable.setColumnWidth(0, 200)
		self.playlistTable.clear()
		self.playlistTable.setRowCount(len(items) + 1)
		self.playlistTable.horizontalHeader().setStretchLastSection(True)

		self.qall = widgets.TableWidgetItem('All')
		self.playlistTable.setItem(0, 0, self.qall)
		for i, item in enumerate(items):
			print ('fill ', item.id, item)
			qitem = widgets.TableWidgetItem(str(item), id=item.id, dbitem=item)
			self.playlistTable.setItem(i + 1, 0, qitem)

		self.playlistTable.setHorizontalHeaderLabels(("Name",))


	def fillMusicTable(self, playlist=None):
		if playlist.id == 0:
			items = self.session.query(models.Song).all()
		else:
			playlistfilter = models.Song.playlists.any(models.Playlist.id == self.currentPlaylist.id)
			items = self.session.query(models.Song).filter(playlistfilter)

		self.songTable.setColumnCount(1)
		self.songTable.setColumnCount(1)
		# self.songTable.setColumnWidth(0, 200)
		self.songTable.horizontalHeader().setStretchLastSection(True)
		self.songTable.clear()
		if playlist.id == 0:
			self.songTable.setRowCount(len(items))
		else:
			self.songTable.setRowCount(len(playlist.dbitem.songs))

		for i, item in enumerate(items):
			qitem = widgets.TableWidgetItem(str(item), id=item.id, dbitem=item)
			self.songTable.setItem(i, 0, qitem)
			if i == 0:
				self.songTable.setCurrentItem(qitem)

		self.songTable.setHorizontalHeaderLabels(("Title",))

	def initButton(self):
		self.getIcons()
		self.tablesHided = False

		# Buttons
		# self.setupButton(self.showHideButton, funct=self.ShowHide, style=False)
		self.setupButton(self.playButton, funct=self.PlayPause, icon=self.playicon)
		self.setupButton(self.stopButton, funct=self.Stop, icon=self.stopicon)

		# Sliders
		self.positionSlider.setMaximum(1000)
		self.positionSlider.setToolTip("Position")
		self.positionSlider.sliderMoved.connect(self.setPosition)
		self.positionSlider.valueChanged.connect(self.valueChanged)
		self.positionSlider.sliderPressed.connect(self.sliderPressed)
		self.volumeSlider.setToolTip("Volume")
		self.volumeSlider.setMaximum(100)
		self.volumeSlider.setValue(self.mediaplayer.audio_get_volume())
		self.volumeSlider.valueChanged.connect(self.setVolume)

	def setupButton(self, button, funct=None, icon=None, text=None, style=True):
		if funct is not None:
			button.clicked.connect(funct)
		if icon is not None:
			button.setIcon(icon)
			button.setIconSize(QSize(50, 50))
		if style is True:
			button.setFlat(True)
			button.setStyleSheet("color: black; background-color: black")

	def initVLC(self, config):
		self.instance = vlc.Instance()
		self.mediaplayer = self.instance.media_player_new()
		self.mediaplayer.audio_set_volume(config['default_volume'])
		# self.media_event = self.mediaplayer.event_manager()

		# self.media_event.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.vlc_time_changed, self.mediaplayer)

		logging.getLogger("vlc").setLevel(logging.NOTSET)
		logging.getLogger("mpgatofixed32").setLevel(logging.NOTSET)		
		logging.getLogger("core vout").setLevel(logging.NOTSET)

	def initDB(self, config):
		self.session = models.createSession(config)
	# def setupUi(self):
	# 	# self.widget = QWidget(self)
	# 	# self.setCentralWidget(self.widget)
	# 	super().setupUi(self)
	# 	# self.widget.setLayout(self.gridLayout)

	def getIcons(self):
		self.playicon = self.getImage('player', 'play.png')
		self.pauseicon = self.getImage('player', 'pause.png')
		self.stopicon = self.getImage('player', 'stop.png')

	def playListChanged(self, current, prev):
		# if current is None:
		# 	self.playlistTable.setCurrentItem(prev)
		# 	return
		print ('Playlist changed', current.id, current.text())
		self.currentPlaylist = current
		self.fillMusicTable(current)

	def musicDoubleClicked(self, item):
		self.currentMusic = item
		music = item.dbitem
		path = '{}/{}/{}'.format(self.playlistpath, music.playlists[0].name, music.localpath)
		self.setFile(path)

	# def ShowHide(self):
	# 	print ("ShowHide")
	# 	if self.tablesHided is False:
	# 		self.playlistTable.hide()
	# 		self.songTable.hide()
	# 		self.tablesHided = True
	# 		self.resize((self.currentwidth), self.currentheight)
	# 		self.resize((self.currentwidth - 400), self.currentheight)
	# 	else:
	# 		self.playlistTable.show()
	# 		self.songTable.show()
	# 		self.resize(self.currentwidth + 50, self.currentheight)
	# 		self.tablesHided = False

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
			self.playButton.setIcon(self.playicon)
			self.playButton.setText("Play")
			self.isPaused = True
		else:
			if self.mediaplayer.play() == -1:
				self.OpenFile()
				return
			self.mediaplayer.play()
			self.playButton.setIcon(self.pauseicon)
			self.playButton.setText("Pause")
			self.timer.start()
			self.isPaused = False

	def Stop(self):
		"""Stop player
		"""
		self.mediaplayer.stop()
		self.playButton.setIcon(self.playicon)

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
			self.fillMusicTable(self.currentPlaylist)

	def addPlaylist(self):
		dialog = widgets.AddPlaylistDialog(self)
		ok = dialog.showDialog()
		if ok:
			name = dialog.getText()
			path = self.playlistpath + '/' + name
			newPlaylist = models.Playlist(name=name)
			os.makedirs(self.playlistpath + '/' + name, exist_ok=True)
			print (newPlaylist)
			self.session.add(newPlaylist)
			self.session.commit()
			self.fillPlaylistTable()
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

	def getTimeString(self, time_ms):
		ms = time_ms % 1000
		seconds = int(time_ms / 1000) % 60
		minutes = int(time_ms / 1000 / 60) % 60
		hours = int(time_ms / 1000 / 60 / 60)

		if seconds < 10:
			seconds = "0" + str(seconds)
		if minutes < 10:
			minutes = "0" + str(minutes)

		print (minutes, seconds)

		string = "{}:{}:{}".format(hours, minutes, seconds)

		return string

	def updateUI(self):
		"""updates the user interface"""
		# setting the slider to the desired position
		self.positionSlider.setValue(self.mediaplayer.get_position() * 1000)

		# print ('', self.mediaplayer.get_time())
		timeString = self.getTimeString(self.mediaplayer.get_time())
		self.currentTime.setText(timeString)

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

	def valueChanged(self, t):
		self.positionvalue = t
		# print (t)

	def resizeEvent(self, resizeEvent):
		self.currentwidth = resizeEvent.size().width()
		self.currentheight = resizeEvent.size().height()

		# self.playlistTable.setColumnWidth(0, self.playlistTable.geometry().width())
		# self.songTable.setColumnWidth(0, self.songTable.geometry().width())

		# self.playlistTable.resize(self.playlistTable.geometry().width())
		# print ("The window has been resized - ", self.currentwidth, self.currentheight)

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
    window = BadPlayer(config)
    # window.show()
    sys.exit(app.exec_())
