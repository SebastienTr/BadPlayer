from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from app.ui.Downloader import Ui_Downloader
import sys
import os
import threading
import urllib.request # just for test

import youtube_dl

import app.badmodels as models

import time

dlThread = dict()
hWindow = 0
fProgressCounter = 0.0
info = None

class DLItem(QObject):
	"""This class is a representation of a downloading element"""
	def __init__(self, parent, url=None, id=0):
		super(DLItem, self).__init__()
		self.url = url
		self.parent = parent
		self.id = id

		self.hSignals = sigHandling(self.id)
		self.hSignals.dlProgress_update.connect(self.hSignals.pbar_incrementer)
		self.hSignals.dlProgress_done.connect(self.hSignals.dlDone)

		rowPosition = self.parent.tableWidget.rowCount()
		self.parent.tableWidget.insertRow(rowPosition)

		self.sizeitem = QTableWidgetItem('')
		self.progressitem = QTableWidgetItem('')
		self.timeitem = QTableWidgetItem('')
		self.titleitem = QTableWidgetItem('')
		self.speeditem = QTableWidgetItem('')
		self.urlitem = QTableWidgetItem(url)

		self.parent.tableWidget.setItem(rowPosition, 0, self.titleitem)
		self.parent.tableWidget.setItem(rowPosition, 1, self.sizeitem)
		self.parent.tableWidget.setItem(rowPosition, 2, self.progressitem)
		self.parent.tableWidget.setItem(rowPosition, 3, self.speeditem)
		self.parent.tableWidget.setItem(rowPosition, 4, self.timeitem)
		self.parent.tableWidget.setItem(rowPosition, 5, self.urlitem)

		global dlThread

		dlThread[self.id] = threading.Thread(target=self.hSignals.runDL,args=(self.url,self.parent.parent.library.playlistpath))
		dlThread[self.id].start()


class Downloader(QMainWindow, Ui_Downloader):
	"""docstring for Downloader"""
	def __init__(self, parent):
		super(Downloader, self).__init__()
		self.parent = parent

		global hWindow
		hWindow = self

		self.setupUi(self)
		# self.tableWidget.horizontalHeader().setStretchLastSection(True)

		self.items = list()
		self.lastId = 0

	def download(self, url, playlist):
		self.playlist = playlist
		self.show()

		if url == "" or playlist is None:
			QMessageBox.information(self, "Empty URL",
					"Please enter the URL of the file you want to download.")
			return

		self.lastId += 1
		dlitem = DLItem(self, url=url, id=self.lastId)
		self.items.append(dlitem)

		return

	def pbarIncValue(self, val, id):
		global fProgressCounter, info
		item = self.getById(id)

		if item is not None:
			item.progressitem.setText(info['_percent_str'])
			item.sizeitem.setText(info['_total_bytes_str'] if info['_total_bytes_str'] is not None else info['_total_bytes_estimate_str'])
			item.speeditem.setText(info['_speed_str'])
			item.timeitem.setText(info['_eta_str'])
			item.titleitem.setText(os.path.basename(info['filename']))

		if self.pbar.value() >= 100:
			# self.dlProgress_done.emit()
			return
		if fProgressCounter > 1.0: # FIX
			self.pbar.setValue(val)
			# self.pbar.setValue(self.pbar.value() + 1)
			fProgressCounter -= 1.0
			fProgressCounter += val
		else:
			fProgressCounter += val

	def getById(self, id):
		for item in self.items:
			if item.id == id:
				return item
		return None

	def formatPath(self, path):
		path = path.replace('|', '_')
		path = path.replace('/', '_')
		return path

	def done(self, info):
		webmFile = '{}/{}-{}.{}'.format(self.parent.library.playlistpath, self.formatPath(info['title']), info['id'], 'webm')
		m4aFile = '{}/{}-{}.{}'.format(self.parent.library.playlistpath, self.formatPath(info['title']), info['id'], 'm4a')
		while os.path.exists(webmFile) is True or os.path.exists(m4aFile) is True:
			time.sleep(1)
		print ("ok it's really done now !!!")
		playlist = self.playlist
		filename = '{}/{}-{}.{}'.format(self.parent.library.playlistpath, self.formatPath(info['title']), info['id'], 'mp3')
		playlist.addMedia(filename, source='Youtube')
		# models.add_music(self.parent.session, filename, self.playlistname, self.playlistid, self.parent.playlistpath, source="Youtube")
		self.parent.fillMusicTable(self.parent.currentPlaylist)

class sigHandling(QObject):
	dlProgress_update = pyqtSignal(float)
	dlProgress_done = pyqtSignal()
	info = None

	def __init__(self, id):
		super().__init__()
		self.id = id

	@pyqtSlot(float)
	def pbar_incrementer(self, val):
		hWindow.pbarIncValue(val, self.id)

	@pyqtSlot()
	def dlDone(self):
		hWindow.pbar.setValue(100)
		hWindow.done(self.info)

	def runDL(self, url, playlistpath):
		global dlThread, hWindow, info
		self.playlistpath = playlistpath

		def my_hook(d):
			if d['status'] == 'downloading':
				bytes = d['total_bytes'] if 'total_bytes' in d else d['total_bytes_estimate']
				incAmount = float((100*d['downloaded_bytes']) / bytes)
				global info
				info = d
				self.dlProgress_update.emit(incAmount)
			if d['status'] == 'finished':
				print('Done downloading, now converting ...')
				self.dlProgress_done.emit()


		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'audioformat': "mp3",      # convert to mp3 
			'outtmpl': playlistpath + '/%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
			'logger': MyLogger(self.id),
			'progress_hooks': [my_hook],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			def tryit():
				try:
					self.info = ydl.extract_info(url, download=False)
					# hWindow.initDL(self.info)
					try:
						ydl.download([url])
					except Exception as edl:
						print ("-- EXCEPTON EXCEPTON EXCEPTON EXCEPTON EXCEPTON ")
						print (edl)
						print ("--------------")
				except Exception as einfo:
					print ("EXCEPTON EXCEPTON EXCEPTON EXCEPTON EXCEPTON ")
					print (einfo)
					print ("--------------")
					tryit()
			tryit()
		return

class MyLogger(QObject):
	def __init__(self, id):
		super().__init__()
		self.id = id

	def debug(self, msg):
		print ("DEBUG", self.id, ':', msg)
		pass

	def warning(self, msg):
		print ("WARNING", self.id, ':', msg)
		pass

	def error(self, msg):
		print ("ERROR", self.id, ':', msg)
		pass