from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QObject

import vlc
import logging
import sys
import os

class PlayerInterface(QObject):
	"""Player interface for VLC"""
	def __init__(self, config, parent):
		super().__init__()
		self.config = config
		self.parent = parent

		self.initVLC(config)
		self.played = list()

		self.mediaplayer_list = None
		self.filelist = None
		self.media_list = None


	def initVLC(self, config):
		self.instance = vlc.Instance()
		self.mediaplayer = self.instance.media_player_new()
		# self.mediaplayer_list = self.instance.media_list_player_new()
		self.mediaplayer.audio_set_volume(config['default_volume'])
		self.media_event = self.mediaplayer.event_manager()
		self.media_event.event_attach(vlc.EventType.MediaPlayerEndReached, self.SongFinished, 1)
		self.media_event.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.nextItemSet, 1)
		# self.media_event.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.vlc_time_changed, self.mediaplayer)

		logging.getLogger("vlc").setLevel(logging.NOTSET)
		logging.getLogger("mpgatofixed32").setLevel(logging.NOTSET)		
		logging.getLogger("core vout").setLevel(logging.NOTSET)

		gifpath = os.path.join("app", "images", "player", "animation.gif")
		self.labelframe = QLabel(self.parent)
		self.labelframe.setScaledContents(True)
		self.labelframe.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		self.anim = QMovie(gifpath)
		self.labelframe.setMovie(self.anim)
		self.parent.framelayout.addWidget(self.labelframe)
		self.labelframe.hide()
		self.musicplayed = False

	def PlayPause(self):
		"""Toggle play/pause status
		"""

		if self.mediaplayer_list.is_playing():
			self.mediaplayer_list.pause()
			# self.playButton.setIcon(self.playicon)
			self.parent.playButton.setText("Play")
			self.isPaused = True
			if self.musicplayed is True:
				self.anim.stop()
				self.musicplayed = False
		else:
			if self.mediaplayer_list.play() == -1:
				self.parent.OpenFile()
				return
			self.mediaplayer_list.play()
			# self.playButton.setIcon(self.pauseicon)
			self.parent.playButton.setText("Pause")
			self.parent.timer.start()
			self.isPaused = False
			if self.musicplayed is False:
				self.anim.start()
				self.musicplayed = True


	def Stop(self):
		"""Stop player
		"""
		self.mediaplayer.stop()
		# self.playButton.setIcon(self.playicon)

	def setFiles(self, filelist):
		# print ('New filelist : \n{}'.format(filelist))
		self.mediaplayer_list = None
		self.filelist = None
		self.media_list = None
		self.indicator = 0
		self.mediaplayer.stop()
		self.filelist = filelist

		self.mediaplayer_list = self.instance.media_list_player_new()
		self.mediaplayer_list.set_media_player(self.mediaplayer)
		self.media_list = self.instance.media_list_new()
		for file in filelist:
			# print ('set :', file.getPath())
			self.media_list.add_media(file.getPath())
		self.mediaplayer_list.set_media_list(self.media_list)


		if sys.platform.startswith('linux'): # for Linux using the X Server
			self.mediaplayer.set_xwindow(self.parent.videoframe.winId())
		elif sys.platform == "win32": # for Windows
			self.mediaplayer.set_hwnd(self.parent.videoframe.winId())
		elif sys.platform == "darwin": # for MacOS
			self.mediaplayer.set_nsobject(int(self.parent.videoframe.winId()))

		self.PlayPause()

	@vlc.callbackmethod
	def SongFinished(self, event, status):
		# print ('item finish : ', self.filelist[self.indicator].name)
		self.indicator += 1

	@vlc.callbackmethod
	def nextItemSet(self, event, status):
		# print ('Item changed : ', self.filelist[self.indicator].name)
		filename = self.filelist[self.indicator].getPath()
		extention = os.path.splitext(filename)[1][1:]
		if extention in ("mp3", "wav"):
			# print ('  it\'s a music')
			self.parent.videoframe.hide()
			self.labelframe.show()
			self.musicplayed = True
			self.anim.start()
			# Animation started
		else:
			# print ('  it\'s a video')
			self.musicplayed = False
			self.labelframe.hide()
			self.parent.videoframe.show()

		# print ('duration : ', self.media_list[self.indicator])

		self.mediaplayer.play()

		# print ('mrl : ', self.mediaplayer.get_media().get_mrl())
		# print ('meta : ', self.mediaplayer.get_media().get_meta())
		self.parent.totalTime.setText(self.getTimeString(self.media_list[self.indicator].get_duration()))


	# def setFile(self, filename):
	# 	# print ("SET -> ", filename)
	# 	self.media = self.instance.media_new(filename)
	# 	self.mediaplayer.set_media(self.media)
	# 	self.media.parse()
	# 	self.parent.setWindowTitle(self.media.get_meta(0))

	# 	if sys.platform.startswith('linux'): # for Linux using the X Server
	# 		self.mediaplayer.set_xwindow(self.parent.videoframe.winId())
	# 	elif sys.platform == "win32": # for Windows
	# 		self.mediaplayer.set_hwnd(self.parent.videoframe.winId())
	# 	elif sys.platform == "darwin": # for MacOS
	# 		self.mediaplayer.set_nsobject(int(self.parent.videoframe.winId()))

	# 	extention = os.path.splitext(filename)[1][1:]
	# 	if extention in ("mp3", "wav"):
	# 		self.parent.videoframe.hide()
	# 		self.labelframe.show()
	# 		self.musicplayed = True
	# 		self.anim.start()
	# 		# Animation started
	# 	else:
	# 		self.musicplayed = False
	# 		self.labelframe.hide()
	# 		self.parent.videoframe.show()

	# 		# self.videoframe.
	# 	# print (self.media.get_duration())
	# 	self.parent.totalTime.setText(self.getTimeString(self.media.get_duration()))
	# 	self.PlayPause()
	# 	self.parent.setStatus("Media added to player")

	def setVolume(self, Volume):
		"""Set the volume
		"""
		self.mediaplayer.audio_set_volume(Volume)

	def setPosition(self, position):
		"""Set the position
		"""
		# setting the position to where the slider was dragged
		self.mediaplayer.set_position(position / 1000.0)

	def sliderPressed(self, t=-1):
		self.mediaplayer.set_position(self.positionvalue / 1000.0)

	# def valueChanged(self, t):
	# 	print ('Value changed, new value : ', t)
	# 	if t != 0:
	# 		self.player.positionvalue = t
	# 		print ('- value changed')
	# 	else:
	# 		print ('- value not changed')


	def getAudioVolume(self):
		return self.mediaplayer.audio_get_volume()

	def getTime(self):
		return self.mediaplayer.get_time()

	def getPosition(self):
		return self.mediaplayer.get_position()

	def getTimeString(self, time_ms):
		ms = time_ms % 1000
		seconds = int(time_ms / 1000) % 60
		minutes = int(time_ms / 1000 / 60) % 60
		hours = int(time_ms / 1000 / 60 / 60)

		if seconds < 10:
			seconds = "0" + str(seconds)
		if minutes < 10:
			minutes = "0" + str(minutes)

		# print (minutes, seconds)

		string = "{}:{}:{}".format(hours, minutes, seconds)

		return string
