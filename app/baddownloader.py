from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from app.ui.Downloader import Ui_Downloader
# import urllib.request # just for test
# import threading
import time
import sys
import os

import app.badmodels as models
import app.badparsers as parsers
import app.badnetwork as network

class Downloader(QMainWindow, Ui_Downloader):
	"""docstring for Downloader"""
	def __init__(self, parent):
		super(Downloader, self).__init__()
		self.parent = parent

		# global hWindow
		# hWindow = self

		self.setupUi(self)
		self.menubar = self.parent.menubar;
		self.tableWidget.horizontalHeader().setStretchLastSection(True)

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
		dlitem = network.DLItem(self, url=url, playlist=playlist)
		self.items.append(dlitem)

		return

	def pbarIncValue(self, val, id, info):
		# global fProgressCounter, info
		item = self.getById(id)

		print (info)
		if item is not None:
			item.progressitem.setText(info['_percent_str'])
			item.sizeitem.setText(info['_total_bytes_str'] if info['_total_bytes_str'] is not None else info['_total_bytes_estimate_str'])
			item.speeditem.setText(info['_speed_str'])
			item.timeitem.setText(info['_eta_str'])
			item.titleitem.setText(os.path.basename(info['filename']))
		self.pbar.setValue(val)
		# if self.pbar.value() >= 100:
		# 	# self.dlProgress_done.emit()
		# 	return
		# if fProgressCounter > 1.0: # FIX
		# 	self.pbar.setValue(val)
		# 	# self.pbar.setValue(self.pbar.value() + 1)
		# 	fProgressCounter -= 1.0
		# 	fProgressCounter += val
		# else:
		# 	fProgressCounter += val

	def getById(self, id):
		for item in self.items:
			if item.id == id:
				return item
		return None

	def formatPath(self, path):
		path = path.replace('|', '_')
		path = path.replace('/', '_')
		return path

	# def done(self, info, id):
	# 	print ('Done method')
	# 	filepath = info['filename']

	# 	dlitem = self.getById(id)

	# 	format = '.mp3' if dlitem.format == 'audio' else '.mp4'

	# 	tmpfilename = info['tmpfilename']
	# 	otherfilename = info['filename']
	# 	finalfilename = info['filename'].replace('.webm', '').replace('.mp4', '')
	# 	if dlitem.format == 'video':
	# 		finalfilename = finalfilename[:-5]
	# 		webmfilename = finalfilename + ".webm"
	# 		finalfilename = finalfilename + format
	# 	else:
	# 		# finalfilename = finalfilename[:-4]
	# 		webmfilename = finalfilename + ".webm"
	# 		finalfilename = finalfilename + format
	# 	name = os.path.splitext(os.path.basename(finalfilename))[0]

	# 	while os.path.exists(tmpfilename) or os.path.exists(otherfilename) or os.path.exists(webmfilename):
	# 		time.sleep(0.5)
	# 	playlist = self.playlist

	# 	print (tmpfilename)
	# 	print (otherfilename)
	# 	print (finalfilename)
	# 	print (webmfilename)
	# 	print (name[:-11])
	# 	# artist_name, song_name = self.getTitleAuthor(name[:-11])
	# 	# print ('title', song_name)
	# 	# print ('artist', artist_name)
	# 	# https://www.youtube.com/watch?v=TKHz-_MmH68
	# 	# filename = '{}/{}'.format(self.parent.library.playlistpath, self.formatPath(info['title']), info['id'], 'mp3')
	# 	print ("Add to DB")
	# 	playlist.addMedia(name=name, filename=finalfilename, source='Youtube', sourceurl=dlitem.url)
	# 	print ("ok it's really done now !!!")
	# 	if os.path.exists(finalfilename) is True:
	# 		os.remove(finalfilename)
	# 	# models.add_music(self.parent.session, filename, self.playlistname, self.playlistid, self.parent.playlistpath, source="Youtube")
	# 	self.parent.fillMusicTable(self.parent.currentPlaylist)

	def getTitleAuthor(self, name):
		parser = parsers.YoutubeTitleParser(name)
		return parser.artist_name.replace('-', ''), parser.song_name.replace('-', '')

	def setRow(self, row, url, rowPosition):
		row.sizeitem = QTableWidgetItem('')
		row.progressitem = QTableWidgetItem('')
		row.timeitem = QTableWidgetItem('')
		row.titleitem = QTableWidgetItem('')
		row.speeditem = QTableWidgetItem('')
		row.urlitem = QTableWidgetItem(url)

		self.tableWidget.setItem(rowPosition, 0, row.titleitem)
		self.tableWidget.setItem(rowPosition, 1, row.sizeitem)
		self.tableWidget.setItem(rowPosition, 2, row.progressitem)
		self.tableWidget.setItem(rowPosition, 3, row.speeditem)
		self.tableWidget.setItem(rowPosition, 4, row.timeitem)
		self.tableWidget.setItem(rowPosition, 5, row.urlitem)

