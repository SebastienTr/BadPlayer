from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui.Downloader import Ui_Downloader
import sys
import os
import threading
import urllib.request # just for test

import youtube_dl

import badmodels as models

import time

dlThread = 0
hWindow = 0
fProgressCounter = 0.0

# finish = False

class TableWidgetItem(QTableWidgetItem):
	def __init__(self, item, id=0, dbitem=None):
		super().__init__(item)
		self.id = id
		self.item = item
		self.dbitem = dbitem

class Downloader(QMainWindow, Ui_Downloader):
	"""docstring for Downloader"""
	def __init__(self, parent):
		super(Downloader, self).__init__()
		self.parent = parent

		global hWindow
		hWindow = self

		self.setupUi(self)

	def download(self, url, playlistname, playlistid):
		self.playlistname = playlistname
		self.playlistid = playlistid
		self.show()
		global dlThread

		hSignals = sigHandling()
		hSignals.dlProgress_update.connect(hSignals.pbar_incrementer)
		hSignals.dlProgress_done.connect(hSignals.dlDone)

		if url == "":
			QMessageBox.information(self, "Empty URL",
					"Please enter the URL of the file you want to download.")
			return
		# else:
		# 	filename = str(QFileDialog.getSaveFileName(self, 'Choose the download location and file name', '.')) ## DETECT A CANCEL
		# 	filename = filename[:-6]
		# 	filename = filename.split("('",maxsplit=1)[1]

		# self.bttDL.setEnabled(False)
		dlThread = threading.Thread(target=hSignals.runDL,args=(url,self.parent.playlistpath))
		dlThread.start()
		return

	def initDL(self, info):
		pass
		# self.pbartest = QProgressBar()
		# self.tableWidget.setItem(0, 0, QTableWidgetItem(info['title']))
		# self.tableWidget.setItem(0, 1, )
		# self.tableWidget.setCellWidget(0, 2, self.pbartest)

	def pbarIncValue(self, val):
		global fProgressCounter
		#print("pbarIncValue({0})\nfProgressCounter={1}".format(val,fProgressCounter))

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

	def formatPath(self, path):
		path = path.replace('|', '_')
		path = path.replace('/', '_')
		return path

	def done(self, info):
		webmFile = '{}/{}-{}.{}'.format(self.parent.playlistpath, self.formatPath(info['title']), info['id'], 'webm')
		while os.path.exists(webmFile) is True:
			time.sleep(1)
		print ("ok it's really done now !!!")
		filename = '{}/{}-{}.{}'.format(self.parent.playlistpath, self.formatPath(info['title']), info['id'], 'mp3')
		models.add_music(self.parent.session, filename, self.playlistname, self.playlistid, self.parent.playlistpath, source="Youtube")
		self.parent.fillMusicTable(self.parent.currentPlaylist)

class sigHandling(QObject):
	dlProgress_update = pyqtSignal(float)
	dlProgress_done = pyqtSignal()
	info = None

	@pyqtSlot(float)
	def pbar_incrementer(self, val):
		hWindow.pbarIncValue(val)

	@pyqtSlot()
	def dlDone(self):
		print("DOOOONNEEEE !!!!!!!!!!!!!!!!")
		hWindow.pbar.setValue(100)
		hWindow.done(self.info)

	def runDL(self, url, playlistpath):
		#print("in run")
		global dlThread, hWindow
		self.playlistpath = playlistpath
		# def report(block_count, block_size, total_size):
		# 	if block_count == 0:
		# 		#print("block_count == 0")
		# 		self.dlProgress_update.emit(0)
		# 	if (block_count * block_size) == total_size:
		# 		self.dlProgress_done.emit()
		# 	incAmount = float((100*block_size) / total_size)
		# 	#print("BS={0} TS={1} incAmount={2}".format(block_size,total_size,incAmount))
		# 	self.dlProgress_update.emit(incAmount)

		def my_hook(d):
			print ('#################')
			print (d)
			print ('#################')
			if d['status'] == 'downloading':
				print(d['filename'], d['_percent_str'], d['_eta_str'])
			# print ("HOOOK : ", d)
				incAmount = float((100*d['downloaded_bytes']) / d['total_bytes'])
			# #print("BS={0} TS={1} incAmount={2}".format(block_size,total_size,incAmount))
			# print ("#######################", incAmount)
				self.dlProgress_update.emit(incAmount)
			if d['status'] == 'finished':
				print('Done downloading, now converting ...')
				print (d)
				print('\n\n')
				print (self.info)
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
			'logger': MyLogger(),
			'progress_hooks': [my_hook],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			# finish = False
			self.info = ydl.extract_info(url, download=False)
			# hWindow.initDL(self.info)
			ydl.download([url])
			# print (info)



		return
		# urllib.request.urlretrieve(dlLink, filename, reporthook=report)
		# #print("emit dlProgress_done")
		# self.dlProgress_done.emit()
		# #print("about to leave dlThread")
		# pass

class MyLogger(object):
	def debug(self, msg):
		print ("DEBUG", msg)
		# if str(msg).find("Deleting original file"):
			# print ('DELETED MOTHER FUCKER ', finish)
			# finish = True
		pass

	def warning(self, msg):
		print ("WARNING", msg)
		pass

	def error(self, msg):
		print ("ERROR", msg)
		pass
