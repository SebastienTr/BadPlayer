# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/MainWindow_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(974, 502)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.frameTab = QtWidgets.QWidget()
        self.frameTab.setObjectName("frameTab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frameTab)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.videoframe = QtWidgets.QFrame(self.frameTab)
        self.videoframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoframe.setObjectName("videoframe")
        self.horizontalLayout_6.addWidget(self.videoframe)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.frameTab, "")
        self.playlistTab = QtWidgets.QWidget()
        self.playlistTab.setObjectName("playlistTab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.playlistTab)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.playlistTable = QtWidgets.QTableWidget(self.playlistTab)
        self.playlistTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.playlistTable.setObjectName("playlistTable")
        self.playlistTable.setColumnCount(0)
        self.playlistTable.setRowCount(0)
        self.playlistTable.verticalHeader().setVisible(False)
        self.horizontalLayout_7.addWidget(self.playlistTable)
        self.songTable = QtWidgets.QTableWidget(self.playlistTab)
        self.songTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.songTable.setObjectName("songTable")
        self.songTable.setColumnCount(0)
        self.songTable.setRowCount(0)
        self.songTable.verticalHeader().setVisible(False)
        self.horizontalLayout_7.addWidget(self.songTable)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_7)
        self.tabWidget.addTab(self.playlistTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.currentTime = QtWidgets.QLabel(self.centralwidget)
        self.currentTime.setMinimumSize(QtCore.QSize(57, 0))
        self.currentTime.setMaximumSize(QtCore.QSize(57, 16777215))
        self.currentTime.setObjectName("currentTime")
        self.horizontalLayout_8.addWidget(self.currentTime)
        self.positionSlider = QtWidgets.QSlider(self.centralwidget)
        self.positionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.positionSlider.setObjectName("positionSlider")
        self.horizontalLayout_8.addWidget(self.positionSlider)
        self.totalTime = QtWidgets.QLabel(self.centralwidget)
        self.totalTime.setMinimumSize(QtCore.QSize(57, 0))
        self.totalTime.setMaximumSize(QtCore.QSize(57, 16777215))
        self.totalTime.setObjectName("totalTime")
        self.horizontalLayout_8.addWidget(self.totalTime)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_4.addWidget(self.playButton)
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_4.addWidget(self.stopButton)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.volumeSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumeSlider.setMinimumSize(QtCore.QSize(50, 0))
        self.volumeSlider.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout_4.addWidget(self.volumeSlider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAddPlaylist = QtWidgets.QAction(MainWindow)
        self.actionAddPlaylist.setObjectName("actionAddPlaylist")
        self.actionAddMusicFromFile = QtWidgets.QAction(MainWindow)
        self.actionAddMusicFromFile.setObjectName("actionAddMusicFromFile")
        self.actionAddMusicFromYoutube = QtWidgets.QAction(MainWindow)
        self.actionAddMusicFromYoutube.setObjectName("actionAddMusicFromYoutube")
        self.actionAddMusicFromSoundcloud = QtWidgets.QAction(MainWindow)
        self.actionAddMusicFromSoundcloud.setObjectName("actionAddMusicFromSoundcloud")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpenDownloader = QtWidgets.QAction(MainWindow)
        self.actionOpenDownloader.setObjectName("actionOpenDownloader")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAddPlaylist)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAddMusicFromFile)
        self.menuFile.addAction(self.actionAddMusicFromYoutube)
        self.menuFile.addAction(self.actionAddMusicFromSoundcloud)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpenDownloader)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.frameTab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.playlistTab), _translate("MainWindow", "Tab 2"))
        self.currentTime.setText(_translate("MainWindow", "00:00:00"))
        self.totalTime.setText(_translate("MainWindow", "00:00:00"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.label_2.setText(_translate("MainWindow", "1:56:42 / 2:26:42"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionAddPlaylist.setText(_translate("MainWindow", "Add playlist"))
        self.actionAddMusicFromFile.setText(_translate("MainWindow", "Add music from file"))
        self.actionAddMusicFromYoutube.setText(_translate("MainWindow", "Add music from Youtube"))
        self.actionAddMusicFromSoundcloud.setText(_translate("MainWindow", "Add music from Soundcloud"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionOpenDownloader.setText(_translate("MainWindow", "Open downloader"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

