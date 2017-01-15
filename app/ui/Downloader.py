# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/ui/Downloader.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Downloader(object):
    def setupUi(self, Downloader):
        Downloader.setObjectName("Downloader")
        Downloader.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(Downloader)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pbar = QtWidgets.QProgressBar(self.centralwidget)
        self.pbar.setProperty("value", 0)
        self.pbar.setObjectName("pbar")
        self.verticalLayout.addWidget(self.pbar)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        Downloader.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Downloader)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        Downloader.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Downloader)
        self.statusbar.setObjectName("statusbar")
        Downloader.setStatusBar(self.statusbar)

        self.retranslateUi(Downloader)
        QtCore.QMetaObject.connectSlotsByName(Downloader)

    def retranslateUi(self, Downloader):
        _translate = QtCore.QCoreApplication.translate
        Downloader.setWindowTitle(_translate("Downloader", "Downloader"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Downloader", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Downloader", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Downloader", "Size"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Downloader", "Progress"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Downloader", "Time"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Downloader", "url"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Downloader = QtWidgets.QMainWindow()
    ui = Ui_Downloader()
    ui.setupUi(Downloader)
    Downloader.show()
    sys.exit(app.exec_())

