from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, Table, Text

from PyQt5.QtCore import QAbstractListModel

import os
from shutil import copyfile

Base = declarative_base()

songsinplaylist = Table('songsinplaylist', Base.metadata,
	Column('playlist_id', ForeignKey('playlist.id'), primary_key=True),
	Column('song_id', ForeignKey('song.id'), primary_key=True)
)

class Playlist(Base):
	"""Playlist entity"""

	__tablename__ = "playlist"

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	songs = relationship('Song', secondary=songsinplaylist, back_populates='playlists')

	def __str__(self):
		return self.name

class PlaylistListModel(QAbstractListModel):

    def __init__(self, session, parent = None):
        QAbstractListModel.__init__(self, parent)
        self.session = session
        self.refresh()

    def rowCount(self, parent):
        return len(self.playlists)

    def refresh(self):
        self.playlists = self.session.query(Playlist).all()

class Song(Base):
	"""Song entity"""

	__tablename__ = "song"

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	source = Column(String(255))
	sourceurl = Column(String(1024), nullable=True)
	localpath = Column(String(1024), unique=True, nullable=False)
	playlists = relationship('Playlist', secondary=songsinplaylist, back_populates='songs')

	def __str__(self):
		return self.name

def createEngine(dbpath):
	# dbpath = "{}/{}".format(os.path.realpath(os.path.dirname(__file__)), config['path'])
	sqlitepath = "sqlite:///{}".format(dbpath)

	engine = create_engine(sqlitepath)
	Base.metadata.create_all(engine)
	return engine

def createSession(dbpath):
	engine = createEngine(dbpath)
	# engine = create_engine('sqlite:///' + config["path"])
	Session = sessionmaker(bind=engine)
	session = Session()
	return session
