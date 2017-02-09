from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import PyQt5 as qt

import app.badwidgets as widgets
import app.badmodels as models
from app.badlibrary import BadLibrary
from app.playerinterface import PlayerInterface

# import logging
import yaml
import sys
import sip
import os

# from ui.MainWindow import Ui_MainWindow
from app.ui.MainWindow import Ui_MainWindow

from app.baddownloader import Downloader

os.environ['VLC_PLUGIN_PATH']='/Applications/VLC.app/Contents/MacOS/plugins'

class BadPlayer(QMainWindow, Ui_MainWindow):
	"""docstring for BadPlayer"""
	def __init__(self, config):
		super(BadPlayer, self).__init__()
		self.title = 'Bad Player'
		# QEvent.accept()
		# self.parent = parent

		self.config = config
		self.clickedPL = None
		self.clickedMusic = None
		self.firstFillPL = True
		self.firstFillSG = True

		self.setupUi(self)
		self.downloader = Downloader(self)

		self.homepath = os.path.expanduser("~")
		self.librarypath = os.path.join(self.homepath, "Music/BadPlayer")
		self.library =  BadLibrary(self.librarypath, self)
		# os.makedirs(self.library.playlistpath, exist_ok=True)

		# self.initVLC(self.config['player'])
		self.player = PlayerInterface(self.config['player'], self)

		self.initUI()
		self.initMenu()
		## Flat design
		# self.setWindowFlags(Qt.FramelessWindowHint)

		self.show()

	def initUI(self):
		self.initButton()
		self.initTables()

		self.timer = QTimer(self)
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.updateUI)
		self.setWindowTitle(self.title)

	def initTables(self):
		self.playlistTable.currentItemChanged.connect(self.playListChanged)
		self.fillPlaylistTable()
		self.playlistTable.setCurrentItem(self.library.itemall.tableItem)
		self.currentPlaylist = self.library.itemall.tableItem

		self.musicTable.itemDoubleClicked.connect(self.musicDoubleClicked)

	def initMenu(self):
		self.actionOpen.triggered.connect(self.OpenFile)
		self.actionExit.triggered.connect(sys.exit)
		self.actionAddPlaylist.triggered.connect(self.addPlaylist)
		self.actionAddMedia.triggered.connect(self.addMedia)
		self.actionOpenDownloader.triggered.connect(self.openDownloader)

	## this function should be externalized
	def fillPlaylistTable(self):
		playlists = self.library.getPlaylists()
		# print (playlists)

		self.playlistTable.setColumnCount(1)
		self.playlistTable.clear()
		self.playlistTable.setRowCount(len(playlists))
		self.playlistTable.horizontalHeader().setStretchLastSection(True)

		for i, playlist in enumerate(playlists):
			# print ('fill ', playlist.id, playlist.name)
			qitem = widgets.TableWidgetItem(playlist)
			self.playlistTable.setItem(i, 0, qitem)

		self.playlistTable.setHorizontalHeaderLabels(("Name",))

	def fillMusicTable(self, selectedPlaylist=None):
		if selectedPlaylist is None:
			selectedPlaylist = self.currentPlaylist
		medias = selectedPlaylist.libraryitem.getMedias()

		self.musicTable.setColumnCount(1)
		self.musicTable.setColumnCount(1)
		self.musicTable.horizontalHeader().setStretchLastSection(True)
		self.musicTable.clear()
		self.musicTable.setRowCount(len(medias))

		for i, media in enumerate(medias):
			qitem = widgets.TableWidgetItem(media)
			self.musicTable.setItem(i, 0, qitem)
			if i == 0:
				self.musicTable.setCurrentItem(qitem)

		self.musicTable.setHorizontalHeaderLabels(("Title",))

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
		self.volumeSlider.setValue(self.player.getAudioVolume())
		self.volumeSlider.valueChanged.connect(self.setVolume)

	def PlayPause(self):
		self.player.PlayPause()

	def Stop(self):
		self.player.mediaplayer.stop()

	def setVolume(self, Volume):
		"""Set the volume
		"""
		self.player.setVolume(Volume)

	def setPosition(self, position):
		"""Set the position
		"""
		self.player.setPosition(position)

	def sliderPressed(self, t=-1):
		self.player.sliderPressed(self.player.positionvalue)

	def valueChanged(self, t):
		self.player.positionvalue = t

	def setupButton(self, button, funct=None, icon=None, text=None, style=True):
		if funct is not None:
			button.clicked.connect(funct)
		if icon is not None:
			button.setIcon(icon)
			button.setIconSize(QSize(50, 50))
		if style is True:
			button.setFlat(True)
			button.setStyleSheet("color: white; background-color: black")

	def getImage(self, folder, filename):
		bpath = os.path.dirname(os.path.realpath(__file__))
		icon = QIcon(QPixmap(os.path.join('app', 'images', folder, filename)))
		# icon = QIcon(QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/images/{}/{}'.format(folder,filename)))
		# print (os.path.dirname(os.path.realpath(__file__)) + '/images/{}/{}'.format(folder,filename))
		return icon

	def openDownloader(self):
		self.downloader.show()

	def getIcons(self):
		self.playicon = self.getImage('player', 'play.png')
		self.pauseicon = self.getImage('player', 'pause.png')
		self.stopicon = self.getImage('player', 'stop.png')

	def playListChanged(self, current, prev):
		self.currentPlaylist = current
		if current == None:
			if self.lastplaylistadd is None:
				self.currentPlaylist = self.library.itemall.tableItem
			else:
				self.currentPlaylist = self.lastplaylistadd
		self.fillMusicTable(self.currentPlaylist)

	def musicDoubleClicked(self, item):
		self.currentMusic = item
		music = item.dbitem
		path = os.path.join(self.library.playlistpath, music.playlists[0].name, music.localpath)
		# path = '{}/{}/{}'.format(self.library.playlistpath, music.playlists[0].name, music.localpath)
		self.player.setFile(path)


	def addMedia(self):
		dialog = widgets.AddMediaDialog(self)
		ok, filename, playlistname, playlistid, index, url = dialog.get()
		if ok:
			if index == 0: # From File
				playlist = self.library.findById(playlistid)
				playlist.addMedia(name=filename, filename=filename, source='File')
				self.fillMusicTable(self.currentPlaylist)
			elif index == 1: # From URL
				playlist = self.library.findById(playlistid)
				self.downloader.download(url, playlist)

	def addPlaylist(self):
		dialog = widgets.AddPlaylistDialog(self)
		ok = dialog.showDialog()
		if ok:
			name = dialog.getText()
			playlist = self.library.addPlaylist(name)
			self.currentPlaylist = playlist
			self.lastplaylistadd = playlist
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

		self.player.setFile(filename)

	def updateUI(self):
		"""updates the user interface"""
		# setting the slider to the desired position
		self.positionSlider.setValue(self.player.getPosition() * 1000)

		# print ('', self.mediaplayer.get_time())
		timeString = self.player.getTimeString(self.player.getTime())
		self.currentTime.setText(timeString)

		if not self.player.mediaplayer.is_playing():
			# no need to call this function if nothing is played
			self.timer.stop()
			if not self.player.isPaused:
				self.player.Stop()

	def setStatus(self, message):
		if message is None:
			self.statusBar().hide()
		else:
			self.statusBar().showMessage(message)

	## Need play/pause for the Space key event
	def keyPressEvent(self, e):
		# self.setStatus("event : " + e.text())
		# print (e)
		if e.text() == ' ':
			self.player.PlayPause()
		if e.key() == Qt.Key_Escape:
			self.close()

def loadConfig():
	config = None
	configpath = "config.yml"
	with open(configpath, 'r') as stream:
		try:
			config = yaml.load(stream)
		except yaml.YAMLError as exc:
			print ("Wrong config file '{}'".format(configpath) + str(exc))
			os._exit(1)
	return config

def main():
    app = QApplication(sys.argv)
    config = loadConfig()
    window = BadPlayer(config)
    sys.exit(app.exec_())
