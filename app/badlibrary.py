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
		self.printMe()

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


		
class BadPlaylist(object):
	"""A BadPlaylist is an element allowed to interact with the Playlist model"""
	def __init__(self, playlist, parent):
		self.session = parent.session
		self.library = parent
		self.tableItem = None
		if playlist == "All":
			self.dbitem = None
			self._name = "All"
			self._id = 0
			medias = list(self.session.query(models.Song).all())
			# medias = models.Song.query.order_by(desc(models.Song.id)).all()
		else:
			self.dbitem = playlist
			self._name = playlist.name
			self._id = playlist.id
			filter = models.Song.playlists.any(models.Playlist.id == self._id)
			medias = list(self.session.query(models.Song).filter(filter))

		# print (medias.reverse())
		# medias = medias.reverse()
		# print (medias.reverse.order_by(desc(models.Song.id)))

		self.medias = list()
		for media in medias:
			self.medias.append(BadMedia(media, self, self.session))

	def addMedia(self, filename, source="File"):
		# playlist = self.library.findById(playlistid)
		name = os.path.basename(filename)
		namewithoutext = os.path.splitext(name)[0]
		path = os.path.join(self.library.playlistpath, self.name)
		path = os.path.join(path, os.path.basename(name))
		shutil.copy(filename, path)
		newmedia = models.Song(name=namewithoutext, source=source, localpath=name)
		newmedia.playlists.append(self.dbitem)
		self.session.add(newmedia)
		self.session.commit()
		newBadMedia = BadMedia(newmedia, self, self.session)
		self.medias.append(newBadMedia)
		self.library.itemall.medias.append(newBadMedia)

	def getMedias(self):
		return self.medias

	@property
	def name(self):
		return self._name

	@property
	def id(self):
		return self._id

	def setTableItem(self, tableItem):
		self.tableItem = tableItem

	def __str__(self):
		return "<BadLibrary.BadPlaylist {} : {}>".format(self.id, self.name)

	def __repr__(self):
		return self.__str__()
		
class BadMedia(object):
	"""A BadMedia is an element allowed to interact with the Music model"""
	def __init__(self, media, parent, session):
		self.tableItem = None
		self.parent = parent
		self.session = session
		self.dbitem = media
		self.name = media.name
		self.id = media.id

	def setTableItem(self, tableItem):
		self.tableItem = tableItem

	def __str__(self):
		return "<BadLibrary.BadPlaylist.BadMedia {} : {}>".format(self.id, self.name)

	def __repr__(self):
		return self.__str__()
