from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import youtube_dl
import threading

dlThread = dict()
hWindow = 0
# fProgressCounter = 0.0
info = None

class DLItem(QObject):
	"""This class is a representation of a downloading element"""
	def __init__(self, parent, url=None, id=0):
		super(DLItem, self).__init__()
		self.url = url
		self.parent = parent
		self.id = id
		self.format = 'audio' # 'video' 'audio'

		self.hSignals = sigHandling(self.id)
		self.hSignals.dlProgress_update.connect(self.hSignals.pbar_incrementer)
		self.hSignals.dlProgress_done.connect(self.hSignals.dlDone)

		rowPosition = self.parent.tableWidget.rowCount()
		self.parent.tableWidget.insertRow(rowPosition)

		self.parent.setRow(self, url, rowPosition)

		global dlThread, hWindow

		hWindow = self.parent

		ydl_opts = {
			'outtmpl': self.parent.parent.library.playlistpath + '/%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
			'logger': MyLogger(self.id),
			# 'progress_hooks': [my_hook],
			'addmetadata': True,
			'verbose': True
		}
		if self.format == 'audio':
			ydl_opts.update({
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'audioformat': "mp3",      # convert to mp3 
			})
		elif self.format == 'video':
			ydl_opts.update({
				'format': '22/best'
			})
			ydl_opts = {
				'outtmpl': self.parent.parent.library.playlistpath + '/%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
			}


		dlThread[self.id] = threading.Thread(target=self.hSignals.runDL,args=(self.url,ydl_opts))
		dlThread[self.id].start()

class sigHandling(QObject):
	dlProgress_update = pyqtSignal(float)
	dlProgress_done = pyqtSignal()
	info = None

	def __init__(self, id):
		super().__init__()
		self.id = id

	@pyqtSlot(float)
	def pbar_incrementer(self, val):
		hWindow.pbarIncValue(val, self.id, info)

	@pyqtSlot()
	def dlDone(self):
		print ('Done signal recieve in handler')
		hWindow.pbar.setValue(100)
		hWindow.done(info, self.id)

	def runDL(self, url, ydl_opts):
		global dlThread, hWindow, info

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

		ydl_opts['progress_hooks'] = [my_hook]
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			def tryit():
				try:
					# self.info = ydl.extract_info(url, download=False)
					# hWindow.initDL(self.info)
					# print ('--------------------------------------')
					# print (ydl.)
					# print ('--------------------------------------')

					try:
						print (ydl.download([url]))
					except Exception as edl:
						print ("-- EXCEPTON EXCEPTON EXCEPTON EXCEPTON EXCEPTON ")
						print (edl)
						print ("--------------")
				except Exception as einfo:
					print ("EXCEPTON EXCEPTON EXCEPTON EXCEPTON EXCEPTON ")
					print (einfo)
					print ("--------------")
					tryit()
			print (ydl.download([url]))
			print ('--------------------------------------------------------')
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
