from PyQt5.QtCore import QObject

import app.badwidgets as widgets
import app.badmodels as models

import os
import shutil

class BadLibrary(QObject):
	"""A BadLibrary is a path to a folder that contain a database and a playlists folder"""
	def __init__(self, path, parent):
		self.path = path
		self.parent = parent

		self.playlistpath = os.path.join(self.path, "playlists")
		self.dbpath = os.path.join(self.path, "db.sqlite3")
		self.session = models.createSession(self.dbpath)

		os.makedirs(self.playlistpath, exist_ok=True)
		self.downloadpath = os.path.join(self.path, 'downloads')
		os.makedirs(self.downloadpath, exist_ok=True)

		self.refresh()
		# self.printMe()

	def refresh(self):
		self.playlists = list()
		self.itemall = BadPlaylist("All", self)
		self.playlists.append(self.itemall)

		playlists = self.session.query(models.Playlist).all()
		for playlist in playlists:
			self.playlists.append(BadPlaylist(playlist, self))

	def getPlaylists(self):
		return self.playlists

	def findByName(self, name):
		for playlist in self.playlists:
			if playlist.name == name:
				return playlist
		return None

	def findById(self, id):
		for playlist in self.playlists:
			if playlist.id == id:
				return playlist
		return None

	def all(self):
		allList = list()
		for playlist in self.playlists:
			allList.extend(playlist.getMedias())
		return allList

	def addPlaylist(self, name):
		newPlaylist = models.Playlist(name=name)
		os.makedirs(self.playlistpath + '/' + name, exist_ok=True)
		self.session.add(newPlaylist)
		self.session.commit()
		playlist = BadPlaylist(newPlaylist, self)
		self.playlists.append(playlist)

	def printMe(self):
		print ('| Library name : ', os.path.basename(self.path))
		print ('| Library path : ', self.path)
		for playlist in self.playlists:
			if playlist.name != "All":
				print ('__|')
				print ('  |___ {} ({})'.format(playlist.name, len(playlist.medias)))
				for media in playlist.medias:
					rest = ''
					if len(media.name) > 80:
						rest = '...'
					print ('    | - {}{}'.format(media.name[:80], rest))



class BadItem(object):
	"""docstring for BadItem"""
	def __init__(self, parent):
		self.parent = parent
		self.session = parent.session
		self.tableItem = None

	def setTableItem(self, tableItem):
		self.tableItem = tableItem

	@property
	def name(self):
		return self._name

	@property
	def id(self):
		return self._id


		
class BadPlaylist(BadItem):
	"""A BadPlaylist is an element allowed to interact with the Playlist model"""
	def __init__(self, playlist, parent):
		super().__init__(parent)
		self.tableItem = None
		if playlist == "All":
			self.dbitem = None
			self._name = "All"
			self._id = 0
			# medias = self.Song.query()
			medias = list(self.session.query(models.Song).order_by(models.Song.id.desc()).all())
			# medias = models.Song.query.order_by(desc(models.Song.id)).all()
		else:
			self.dbitem = playlist
			self._name = playlist.name
			self._id = playlist.id
			filter = models.Song.playlists.any(models.Playlist.id == self._id)
			medias = list(self.session.query(models.Song).filter(filter).order_by(models.Song.id.desc()))

		self.medias = list()
		for media in medias:
			self.medias.append(BadMedia(media, self, self.session))

	def addMedia(self, name, filename, source="File", sourceurl=None):
		# playlist = self.library.findById(playlistid)
		name = os.path.basename(filename)
		# namewithoutext = os.path.splitext(name)[0]
		path = os.path.join(self.parent.playlistpath, self.name)
		path = os.path.join(path, os.path.basename(name))
		print ("- Copy", filename, 'to', path)
		if os.path.exists(path) is not True:
			try:
				shutil.copy(filename, path)
			except Exception as e:
				pass
		newmedia = models.Song(name=name, source=source, localpath=name, sourceurl=sourceurl)
		newmedia.playlists.append(self.dbitem)
		self.session.add(newmedia)
		self.session.commit()
		newBadMedia = BadMedia(newmedia, self, self.session)
		self.medias.append(newBadMedia)
		self.parent.itemall.medias.append(newBadMedia)

	def getMedias(self):
		return self.medias

	def __str__(self):
		return "<BadLibrary.BadPlaylist {} : {}>".format(self.id, self.name)

	def __repr__(self):
		return self.__str__()
		


class BadMedia(BadItem):
	"""A BadMedia is an element allowed to interact with the Music model"""
	def __init__(self, media, parent, session):
		super().__init__(parent)
		self.tableItem = None
		self.parent = parent
		self.session = session
		self.dbitem = media
		self._name = media.name
		self._id = media.id

	def __str__(self):
		return "<BadLibrary.BadPlaylist.BadMedia {} : {}>".format(self.id, self.name)

	def __repr__(self):
		return self.__str__()
