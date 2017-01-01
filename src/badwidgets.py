from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import badmodels as models
import random
from ui.AddFileDialog import Ui_AddFileDialog

import os
import sys

# class ListWidgetItem(QListWidgetItem):
# 	def __init__(self, item, id=0, dbitem=None):
# 		super(ListWidgetItem, self).__init__(item)
# 		self.id = id
# 		self.item = item
# 		self.dbitem = dbitem

class TableWidgetItem(QTableWidgetItem):
	def __init__(self, item, id=0, dbitem=None):
		super().__init__(item)
		self.id = id
		self.item = item
		self.dbitem = dbitem

# class ExtendedQLabel(QLabel):
# 	def __init__(self, parent):
# 		QLabel.__init__(self, parent)

# 	def mouseReleaseEvent(self, ev):
# 		self.emit(SIGNAL('clicked()'))

class ListWidget(QWidget):
	"""docstring for player"""
	def __init__(self, parent, model, fill=True):
		super().__init__()
		self.parent = parent
		self.model = model
		self.session = self.parent.session

		self.initUI(fill)

	def initUI(self, fill):
		layout = QHBoxLayout()
		self.list = QListWidget()
		if fill: self.fill()
		layout.addWidget(self.list)
		self.setLayout(layout)

	def refresh(self):
		self.list.clear()
		self.fill()

	def fill(self):
		items = self.parent.session.query(self.model).all()
		qitem = ListWidgetItem('All')
		self.list.insertItem(0, qitem)
		# self.list.insertItem
		for i, item in enumerate(items):
			qitem = ListWidgetItem(str(item), id=item.id)
			self.list.insertItem(items[i].id, qitem)

class SongsWidget(ListWidget):
	"""docstring for SongsWidget"""
	def __init__(self, parent, model):
		super().__init__(parent, model, fill=False)
		self.parent = parent
		self.model = model
		self.playlist = None
		self.list.itemDoubleClicked.connect(self.item_doubleclicked)

	def fill(self, playlist):
		self.list.clear()
		self.playlist = playlist
		if playlist.id == 0:
			items = self.parent.session.query(self.model).all()
			# items = random.shuffle(items)
		else:
			items = self.parent.session.query(self.model).filter(self.model.playlists.any(models.Playlist.id == playlist.id))
		for i, item in enumerate(items):
			qitem = ListWidgetItem(str(item), id=item.id, dbitem=item)
			self.list.insertItem(items[i].id, qitem)

	def item_doubleclicked(self, item):
		song = item.dbitem
		path = '{}/{}/{}'.format(self.parent.playlistpath, song.playlists[0].name, song.localpath)
		self.parent.setFile(path)

class PlaylistsWidget(ListWidget):
	"""docstring for SongsWidget"""
	def __init__(self, parent, model, songslist):
		super().__init__(parent, model, fill=True)
		self.parent = parent
		self.model = model
		self.songslist = songslist
		self.list.currentItemChanged.connect(self.item_click)

	def item_click(self, current, prev):
		# print ('hehe', current.text())
		# print ('Item changed :', current.text(), current.id)
		self.parent.clickedPL = current
		self.songslist.fill(current)


class AddPlaylistDialog(QWidget):
	"""docstring for AddPlaylistDialog"""
	def __init__(self, parent=None):
		super(AddPlaylistDialog, self).__init__()
		self.parent = parent
		self.text = None

	def showDialog(self):
		
		text, ok = QInputDialog.getText(self, 'Add new playlist', 
			'Playlist name :')
		
		if ok:
			self.__text = text
			return True
		else:
			return False

	def getText(self):
		return self.__text

# class AddSongDialog(QWidget):
# 	"""docstring for AddPlaylistDialog"""
# 	def __init__(self, parent=None):
# 		super(AddPlaylistDialog, self).__init__()
# 		self.parent = parent
# 		self.text = None

# 	def showDialog(self):
		
# 		text, ok = QInputDialog.getText(self, 'Add new playlist', 
# 			'Playlist name :')
		
# 		if ok:
# 			self.__text = text
# 			return True
# 		else:
# 			return False

# 	def getText(self):
# 		return self.__text

class AddSongDialog(Ui_AddFileDialog):
	def __init__(self, parent):
		Ui_AddFileDialog.__init__(self)
		self.dialog = QDialog()
		self.parent = parent
		self.filename = None
		self.initUI()

	def initUI(self):
		self.setupUi(self.dialog)
		self.openfilebutton.clicked.connect(self.OpenFile)

		playlistsItems = self.parent.session.query(models.Playlist).all()
		for item in playlistsItems:
			self.playlistBox.addItem(item.name, userData=item.id)



	def get(self):
		ok = self.dialog.exec_()
		playlistname = self.playlistBox.currentText()
		playlistid = self.playlistBox.currentData()

		return ok, self.filename, playlistname, playlistid

	def OpenFile(self, filename=None):
		"""Open a media file in a MediaPlayer
		"""
		filename=None
		if filename is None:
			fdialog = QFileDialog()
			# fdialog.selectMimeTypeFilter(("*.mp3"))
			filename = fdialog.getOpenFileName(self.parent, "Open File", os.path.expanduser('~'))[0]
		if not filename:
			return
		if sys.version < '3': 
			filename = unicode(filename)
		self.filename = filename

		self.pathLabel.setText(filename)


# class AddSongDialog(QDialog):
#     def __init__(self, parent = None):
#         super(AddSongDialog, self).__init__(parent)

#         layout = QVBoxLayout(self)

#         # nice widget for editing the date
#         self.datetime = QDateTimeEdit(self)
#         self.datetime.setCalendarPopup(True)
#         self.datetime.setDateTime(QDateTime.currentDateTime())
#         layout.addWidget(self.datetime)

#         # OK and Cancel buttons
#         buttons = QDialogButtonBox(
#             QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
#             Qt.Horizontal, self)
#         buttons.accepted.connect(self.accept)
#         buttons.rejected.connect(self.reject)
#         layout.addWidget(buttons)

#     # get current date and time from the dialog
#     def dateTime(self):
#         return self.datetime.dateTime()

#     # static method to create the dialog and return (date, time, accepted)
#     @staticmethod
#     def getDateTime(parent = None):
#         dialog = AddSongDialog(parent)
#         result = dialog.exec_()
#         date = dialog.dateTime()
#         return (date.date(), date.time(), result == QDialog.Accepted)
