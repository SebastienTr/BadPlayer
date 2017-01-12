# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/AddFileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddFileDialog(object):
    def setupUi(self, AddFileDialog):
        AddFileDialog.setObjectName("AddFileDialog")
        AddFileDialog.resize(470, 401)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AddFileDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.playlistBox = QtWidgets.QComboBox(AddFileDialog)
        self.playlistBox.setObjectName("playlistBox")
        self.verticalLayout_2.addWidget(self.playlistBox)
        self.tabWidget = QtWidgets.QTabWidget(AddFileDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.fromFile = QtWidgets.QWidget()
        self.fromFile.setObjectName("fromFile")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.fromFile)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileLabel = QtWidgets.QLabel(self.fromFile)
        self.fileLabel.setMaximumSize(QtCore.QSize(16777215, 100))
        self.fileLabel.setObjectName("fileLabel")
        self.verticalLayout.addWidget(self.fileLabel)
        self.openfilebutton = QtWidgets.QPushButton(self.fromFile)
        self.openfilebutton.setObjectName("openfilebutton")
        self.verticalLayout.addWidget(self.openfilebutton)
        self.tabWidget.addTab(self.fromFile, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.url = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.url.sizePolicy().hasHeightForWidth())
        self.url.setSizePolicy(sizePolicy)
        self.url.setObjectName("url")
        self.verticalLayout_3.addWidget(self.url)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddFileDialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(AddFileDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(AddFileDialog.accept)
        self.buttonBox.rejected.connect(AddFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddFileDialog)

    def retranslateUi(self, AddFileDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFileDialog.setWindowTitle(_translate("AddFileDialog", "Dialog"))
        self.fileLabel.setText(_translate("AddFileDialog", "Open a file"))
        self.openfilebutton.setText(_translate("AddFileDialog", "Open"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fromFile), _translate("AddFileDialog", "File"))
        self.label.setText(_translate("AddFileDialog", "Enter a youtube url"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AddFileDialog", "URL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddFileDialog = QtWidgets.QDialog()
    ui = Ui_AddFileDialog()
    ui.setupUi(AddFileDialog)
    AddFileDialog.show()
    sys.exit(app.exec_())

