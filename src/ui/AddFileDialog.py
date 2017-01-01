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
        AddFileDialog.resize(330, 233)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddFileDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 200, 271, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(AddFileDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 291, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.playlistBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.playlistBox.setObjectName("playlistBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.playlistBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.openfilebutton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.openfilebutton.setObjectName("openfilebutton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.openfilebutton)
        self.pathLabel = QtWidgets.QLabel(AddFileDialog)
        self.pathLabel.setGeometry(QtCore.QRect(20, 95, 281, 81))
        self.pathLabel.setText("")
        self.pathLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.pathLabel.setWordWrap(True)
        self.pathLabel.setObjectName("pathLabel")

        self.retranslateUi(AddFileDialog)
        self.buttonBox.accepted.connect(AddFileDialog.accept)
        self.buttonBox.rejected.connect(AddFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddFileDialog)

    def retranslateUi(self, AddFileDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFileDialog.setWindowTitle(_translate("AddFileDialog", "Dialog"))
        self.label.setText(_translate("AddFileDialog", "Playlist"))
        self.label_2.setText(_translate("AddFileDialog", "File"))
        self.openfilebutton.setText(_translate("AddFileDialog", "open file"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddFileDialog = QtWidgets.QDialog()
    ui = Ui_AddFileDialog()
    ui.setupUi(AddFileDialog)
    AddFileDialog.show()
    sys.exit(app.exec_())

