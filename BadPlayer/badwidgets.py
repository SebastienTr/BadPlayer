from PyQt5.QtWidgets import (QWidget,
							QHBoxLayout,
							QFrame,
							QSplitter)

class PlayerWidget(QWidget):
	"""docstring for player"""
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

		self.initPlayer()
		
	def initPlayer(self):
		"""Set up the user interface, signals & slots
		"""
		hbox = QHBoxLayout(self)

		topleft = QFrame(self)
		topleft.setFrameShape(QFrame.StyledPanel)

		topright = QFrame(self)
		topright.setFrameShape(QFrame.StyledPanel)

		bottom = QFrame(self)
		bottom.setFrameShape(QFrame.StyledPanel)

		splitter1 = QSplitter(Qt.Horizontal)
		splitter1.addWidget(topleft)
		splitter1.addWidget(topright)

		splitter2 = QSplitter(Qt.Vertical)
		splitter2.addWidget(splitter1)
		splitter2.addWidget(bottom)

		hbox.addWidget(splitter2)
		self.setLayout(hbox)

	def onChanged(self, text):

		self.lbl.setText(text)
		self.lbl.adjustSize() 