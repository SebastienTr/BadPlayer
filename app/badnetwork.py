from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import youtube_dl
import threading

import os, time

dlThread = dict()
hWindow = 0
# fProgressCounter = 0.0
info = None

class DLItem(QObject):
	"""This class is a representation of a downloading element"""
	def __init__(self, parent, url=None, id=0, playlist=None):
		super(DLItem, self).__init__()
		self.url = url
		self.parent = parent
		self.id = id
		self.format = 'audio' # 'video' 'audio'
		self.playlist = playlist

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


		dlThread[self.id] = threading.Thread(target=self.hSignals.runDL,args=(self.url, self, ydl_opts))
		dlThread[self.id].start()

	def done(self, info):
		print ('Done method')
		filepath = info['filename']

		# dlitem = self.getById(id)

		format = '.mp3' if self.format == 'audio' else '.mp4'

		tmpfilename = info['tmpfilename']
		otherfilename = info['filename']
		finalfilename = (info['filename'].replace('.webm', '')
										.replace('.mp4', '')
										.replace('.m4a', '')
										.replace('.part', '')
										)
		if self.format == 'video':
			# finalfilename = finalfilename[:-5]
			webmfilename = finalfilename + ".webm"
			finalfilename = finalfilename + format
		else:
			# finalfilename = finalfilename[:-4]
			webmfilename = finalfilename + ".webm"
			finalfilename = finalfilename + format
		name = os.path.splitext(os.path.basename(finalfilename))[0]

		while os.path.exists(tmpfilename) or os.path.exists(otherfilename) or os.path.exists(webmfilename):
			time.sleep(0.5)

		print ('tmpfilename :', tmpfilename)
		print ('otherfilename :', otherfilename)
		print ('finalfilename :', finalfilename)
		print ('webmfilename :', webmfilename)
		print ('name :', name)
		# artist_name, song_name = self.getTitleAuthor(name[:-11])
		# print ('title', song_name)
		# print ('artist', artist_name)
		# https://www.youtube.com/watch?v=TKHz-_MmH68
		# filename = '{}/{}'.format(self.parent.library.playlistpath, self.formatPath(info['title']), info['id'], 'mp3')
		print ("Add to DB")
		self.playlist.addMedia(name=name, filename=finalfilename, source='Youtube', sourceurl=self.url)
		print ("ok it's really done now !!!")
		if os.path.exists(finalfilename) is True:
			os.remove(finalfilename)
		# models.add_music(self.parent.session, filename, self.playlistname, self.playlistid, self.parent.playlistpath, source="Youtube")
		self.parent.parent.fillMusicTable(self.parent.parent.currentPlaylist)

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
		# hWindow.done(info, self.id)
		self.item.done(info)

	def runDL(self, url, item, ydl_opts):
		global dlThread, hWindow, info

		self.item = item

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
