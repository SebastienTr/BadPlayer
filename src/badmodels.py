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

    # def data(self, index, role):
    #     users = get_users(self.session)

    #     # Only for debug
    #     print(users)

    #     if role == QtCore.Qt.DisplayRole:
    #         value = users[index.row()]
    #         return "%s : %s" % (value.id_, value.name)

class Song(Base):
	"""Song entity"""

	__tablename__ = "song"

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	source = Column(String(255))
	sourceurl = Column(String(1024), nullable=True)
	localpath = Column(String(1024), unique=True)
	playlists = relationship('Playlist', secondary=songsinplaylist, back_populates='songs')

	def __str__(self):
		return self.name

def add_music(session, filename, playlistname, playlistid, playlistpath, source="File"):
	name = os.path.basename(filename)
	namewithoutext = os.path.splitext(name)[0]
	finalpath = '{}/{}/{}'.format(playlistpath, playlistname, name)
	# print (filename, '--->', finalpath)
	copyfile(filename, finalpath)
	newsong = Song(name=namewithoutext, source=source, localpath=name)
	playlist = session.query(Playlist).get(playlistid)
	newsong.playlists.append(playlist)
	session.add(newsong)
	session.commit()


def createEngine(config):
	dbpath = "{}/{}".format(os.path.realpath(os.path.dirname(__file__)), config['path'])
	sqlitepath = "sqlite:///{}".format(dbpath)

	engine = create_engine(sqlitepath)
	Base.metadata.create_all(engine)
	return engine

def createSession(config):
	engine = createEngine(config)
	# engine = create_engine('sqlite:///' + config["path"])
	Session = sessionmaker(bind=engine)
	session = Session()
	return session
