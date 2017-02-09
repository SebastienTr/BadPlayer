from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from app.ui.AddFileDialog import Ui_AddFileDialog
import app.badmodels as models

import random
import sys
import os

# class ListWidgetItem(QListWidgetItem):
# 	def __init__(self, item, id=0, dbitem=None):
# 		super(ListWidgetItem, self).__init__(item)
# 		self.id = id
# 		self.item = item
# 		self.dbitem = dbitem

class TableWidgetItem(QTableWidgetItem):
	def __init__(self, item):
		super().__init__(item.name)
		self.id = item.id
		self.name = item.name
		self.dbitem = item.dbitem
		self.libraryitem = item

		item.setTableItem(self)

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

class AddMediaDialog(Ui_AddFileDialog):
	def __init__(self, parent):
		Ui_AddFileDialog.__init__(self)
		self.dialog = QDialog()
		self.parent = parent
		self.filename = None
		self.initUI()

	def initUI(self):
		self.setupUi(self.dialog)
		self.openfilebutton.clicked.connect(self.OpenFile)

		playlistsItems = self.parent.library.getPlaylists()
		for item in playlistsItems:
			self.playlistBox.addItem(item.name, userData=item.id)

	def get(self):
		ok = self.dialog.exec_()
		playlistname = self.playlistBox.currentText()
		playlistid = self.playlistBox.currentData()

		index = self.tabWidget.currentIndex()
		url = self.url.text()
		print (url)
		return ok, self.filename, playlistname, playlistid, index, url

	def OpenFile(self, filename=None):
		"""Open a media file in a MediaPlayer
		"""
		filename=None
		if filename is None:
			fdialog = QFileDialog()
			# fdialog.selectMimeTypeFilter(("*.mp3"))
			filters = "Music/Video files (*.mp3 *.wav *.flac *.avi *.mkv *.mp4 *.mov)"
			filename = fdialog.getOpenFileName(self.parent, "Open File", os.path.expanduser('~'), filters)[0]
		if not filename:
			return
		if sys.version < '3': 
			filename = unicode(filename)
		self.filename = filename

		self.fileLabel.setText(filename)
