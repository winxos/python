# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Tue Mar  1 00:31:37 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_wForm(object):
    def setupUi(self, wForm):
        wForm.setObjectName(_fromUtf8("wForm"))
        wForm.resize(552, 291)
        self.widget = QtGui.QWidget(wForm)
        self.widget.setGeometry(QtCore.QRect(9, 9, 534, 273))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnSelect = QtGui.QPushButton(self.widget)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.horizontalLayout_2.addWidget(self.btnSelect)
        self.btnPurge = QtGui.QPushButton(self.widget)
        self.btnPurge.setObjectName(_fromUtf8("btnPurge"))
        self.horizontalLayout_2.addWidget(self.btnPurge)
        self.btnReversion = QtGui.QPushButton(self.widget)
        self.btnReversion.setObjectName(_fromUtf8("btnReversion"))
        self.horizontalLayout_2.addWidget(self.btnReversion)
        self.btnUndo = QtGui.QPushButton(self.widget)
        self.btnUndo.setObjectName(_fromUtf8("btnUndo"))
        self.horizontalLayout_2.addWidget(self.btnUndo)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.txtmsg = QtGui.QPlainTextEdit(self.widget)
        self.txtmsg.setObjectName(_fromUtf8("txtmsg"))
        self.verticalLayout.addWidget(self.txtmsg)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.txtout = QtGui.QTextEdit(self.widget)
        self.txtout.setObjectName(_fromUtf8("txtout"))
        self.verticalLayout_2.addWidget(self.txtout)
        self.btnApply = QtGui.QPushButton(self.widget)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.verticalLayout_2.addWidget(self.btnApply)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(wForm)
        QtCore.QObject.connect(self.btnSelect, QtCore.SIGNAL(_fromUtf8("clicked()")), wForm.openPath)
        QtCore.QObject.connect(self.btnReversion, QtCore.SIGNAL(_fromUtf8("clicked()")), wForm.reVersion)
        QtCore.QObject.connect(self.btnPurge, QtCore.SIGNAL(_fromUtf8("clicked()")), wForm.purge)
        QtCore.QMetaObject.connectSlotsByName(wForm)

    def retranslateUi(self, wForm):
        wForm.setWindowTitle(QtGui.QApplication.translate("wForm", "ProEVersion", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelect.setText(QtGui.QApplication.translate("wForm", "选择文件夹", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPurge.setText(QtGui.QApplication.translate("wForm", "清除旧版本", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReversion.setText(QtGui.QApplication.translate("wForm", "后缀归1", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUndo.setText(QtGui.QApplication.translate("wForm", "清除上次保存", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("wForm", "原始文件", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("wForm", "效果预览", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApply.setText(QtGui.QApplication.translate("wForm", "应用", None, QtGui.QApplication.UnicodeUTF8))

