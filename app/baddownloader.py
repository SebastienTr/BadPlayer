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

import app.badparsers as parsers

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
		self.format = 'audio' # 'video' 'audio'

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

class Downloader(QMainWindow, Ui_Downloader):
	"""docstring for Downloader"""
	def __init__(self, parent):
		super(Downloader, self).__init__()
		self.parent = parent

		global hWindow
		hWindow = self

		self.setupUi(self)
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
		dlitem = DLItem(self, url=url, id=self.lastId)
		self.items.append(dlitem)

		return

	def pbarIncValue(self, val, id):
		global fProgressCounter, info
		item = self.getById(id)

		print (info)
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

	def done(self, info, id):
		print ('Done method')
		filepath = info['filename']

		dlitem = self.getById(id)

		format = '.mp3' if dlitem.format == 'audio' else '.mp4'

		tmpfilename = info['tmpfilename']
		otherfilename = info['filename']
		finalfilename = info['filename'].replace('.webm', '').replace('.mp4', '')
		if dlitem.format == 'video':
			finalfilename = finalfilename[:-5]
		webmfilename = finalfilename + ".webm"
		finalfilename = finalfilename + format
		name = os.path.splitext(os.path.basename(finalfilename))[0]

		while os.path.exists(tmpfilename) or os.path.exists(otherfilename) or os.path.exists(webmfilename):
			time.sleep(0.5)
		playlist = self.playlist

		print (tmpfilename)
		print (otherfilename)
		print (finalfilename)
		print (webmfilename)
		print (name[:-11])
		artist_name, song_name = self.getTitleAuthor(name[:-11])
		print ('title', song_name)
		print ('artist', artist_name)
		# https://www.youtube.com/watch?v=TKHz-_MmH68
		# filename = '{}/{}'.format(self.parent.library.playlistpath, self.formatPath(info['title']), info['id'], 'mp3')
		print ("Add to DB")
		playlist.addMedia(name=name, filename=finalfilename, source='Youtube', sourceurl=dlitem.url)
		print ("ok it's really done now !!!")
		if os.path.exists(finalfilename) is True:
			os.remove(finalfilename)
		# models.add_music(self.parent.session, filename, self.playlistname, self.playlistid, self.parent.playlistpath, source="Youtube")
		self.parent.fillMusicTable(self.parent.currentPlaylist)

	def getTitleAuthor(self, name):
		parser = parsers.YoutubeTitleParser(name)
		return parser.artist_name.replace('-', ''), parser.song_name.replace('-', '')

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
			# tryit()
		################################################################
		# ydl_opts = {
		#     'usenetrc': opts.usenetrc,
		#     'username': opts.username,
		#     'password': opts.password,
		#     # ... all options list available in sources
		#     'exec_cmd': opts.exec_cmd,
		# }
		# with YoutubeDL(ydl_opts) as ydl:
		# 	ydl.print_debug_header()
		# 	ydl.add_default_info_extractors()

		# 	# PostProcessors
		# 	# Add the metadata pp first, the other pps will copy it
		# 	if opts.addmetadata:
		# 		ydl.add_post_processor(FFmpegMetadataPP())
		# 	if opts.extractaudio:
		# 		ydl.add_post_processor(FFmpegExtractAudioPP(preferredcodec=opts.audioformat, preferredquality=opts.audioquality, nopostoverwrites=opts.nopostoverwrites))
		# 	if opts.recodevideo:
		# 		ydl.add_post_processor(FFmpegVideoConvertor(preferedformat=opts.recodevideo))
		# 	if opts.embedsubtitles:
		# 		ydl.add_post_processor(FFmpegEmbedSubtitlePP(subtitlesformat=opts.subtitlesformat))
		# 	if opts.xattrs:
		# 		ydl.add_post_processor(XAttrMetadataPP())
		# 	if opts.embedthumbnail:
		# 		if not opts.addmetadata:
		# 			ydl.add_post_processor(FFmpegAudioFixPP())
		# 		ydl.add_post_processor(AtomicParsleyPP())


		# 	# Please keep ExecAfterDownload towards the bottom as it allows the user to modify the final file in any way.
		# 	# So if the user is able to remove the file before your postprocessor runs it might cause a few problems.
		# 	if opts.exec_cmd:
		# 		ydl.add_post_processor(ExecAfterDownloadPP(
		# 			verboseOutput=opts.verbose, exec_cmd=opts.exec_cmd))

		# 	# Update version
		# 	if opts.update_self:
		# 		update_self(ydl.to_screen, opts.verbose)

		# 	# Remove cache dir
		# 	if opts.rm_cachedir:
		# 		ydl.cache.remove()

		# 	# Maybe do nothing
		# 	if (len(all_urls) < 1) and (opts.load_info_filename is None):
		# 		if not (opts.update_self or opts.rm_cachedir):
		# 			parser.error(u'you must provide at least one URL')
		# 		else:
		# 			sys.exit()

		# 	try:
		# 		if opts.load_info_filename is not None:
		# 			retcode = ydl.download_with_info_file(opts.load_info_filename)
		# 		else:
		# 			retcode = ydl.download(all_urls)
		# 	except MaxDownloadsReached:
		# 		ydl.to_screen(u'--max-download limit reached, aborting.')
		# 		retcode = 101
		# ################################################################
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
