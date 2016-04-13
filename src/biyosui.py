# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'biyos.ui'
#
# Created: Tue Apr 12 20:03:13 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(480, 640)
        self.tum_borclar = QtGui.QPushButton(MainWindow)
        self.tum_borclar.setGeometry(QtCore.QRect(60, 240, 361, 91))
        self.tum_borclar.setObjectName(_fromUtf8("tum_borclar"))
        self.apartman_aidat = QtGui.QPushButton(MainWindow)
        self.apartman_aidat.setGeometry(QtCore.QRect(60, 130, 361, 91))
        self.apartman_aidat.setObjectName(_fromUtf8("apartman_aidat"))
        self.frame = QtGui.QFrame(MainWindow)
        self.frame.setGeometry(QtCore.QRect(40, 350, 391, 251))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 341, 221))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioA = QtGui.QRadioButton(self.groupBox)
        self.radioA.setGeometry(QtCore.QRect(0, 40, 91, 51))
        self.radioA.setObjectName(_fromUtf8("radioA"))
        self.radioB = QtGui.QRadioButton(self.groupBox)
        self.radioB.setGeometry(QtCore.QRect(100, 40, 111, 51))
        self.radioB.setObjectName(_fromUtf8("radioB"))
        self.tekil_borc = QtGui.QPushButton(self.groupBox)
        self.tekil_borc.setGeometry(QtCore.QRect(0, 150, 341, 71))
        self.tekil_borc.setObjectName(_fromUtf8("tekil_borc"))
        self.daire_no = QtGui.QLineEdit(self.groupBox)
        self.daire_no.setGeometry(QtCore.QRect(100, 90, 113, 32))
        self.daire_no.setObjectName(_fromUtf8("daire_no"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 90, 101, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.giris = QtGui.QPushButton(MainWindow)
        self.giris.setGeometry(QtCore.QRect(60, 30, 361, 81))
        self.giris.setObjectName(_fromUtf8("giris"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Form", None))
        self.tum_borclar.setText(_translate("MainWindow", "Tüm kişisel borçları yazdır", None))
        self.apartman_aidat.setText(_translate("MainWindow", "Apartman aidat borçlarını yazdır", None))
        self.groupBox.setTitle(_translate("MainWindow", "Tek borç yazdır", None))
        self.radioA.setText(_translate("MainWindow", "A blok", None))
        self.radioB.setText(_translate("MainWindow", "B blok", None))
        self.tekil_borc.setText(_translate("MainWindow", "Yazdır", None))
        self.label.setText(_translate("MainWindow", "Daire No:", None))
        self.giris.setText(_translate("MainWindow", "mbkaptan@gmail.com ile giriş yap", None))

