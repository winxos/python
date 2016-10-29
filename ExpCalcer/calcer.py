# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CALCER\calcer.ui'
#
# Created: Wed Mar 23 12:18:32 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(500, 303)
        self.btn = QtGui.QPushButton(Form)
        self.btn.setGeometry(QtCore.QRect(10, 253, 481, 40))
        self.btn.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(14)
        self.btn.setFont(font)
        self.btn.setObjectName(_fromUtf8("btn"))
        self.txt = QtGui.QPlainTextEdit(Form)
        self.txt.setGeometry(QtCore.QRect(10, 162, 480, 85))
        self.txt.setObjectName(_fromUtf8("txt"))
        self.txtout = QtGui.QPlainTextEdit(Form)
        self.txtout.setGeometry(QtCore.QRect(10, 41, 480, 84))
        self.txtout.setObjectName(_fromUtf8("txtout"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 131, 114, 25))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 95, 25))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.calc)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "表达式计算器", None, QtGui.QApplication.UnicodeUTF8))
        self.btn.setText(QtGui.QApplication.translate("Form", "计算！", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "输入表达式：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "计算结果：", None, QtGui.QApplication.UnicodeUTF8))

