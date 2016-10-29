# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\LiWei\My Documents\My DBank\programming\mycode\python\ArtChar\ArtCharMaker.ui'
#
# Created: Fri Apr  8 13:26:34 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(459, 296)
        MainWindow.setMinimumSize(QtCore.QSize(459, 296))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.le_chars = QtGui.QLineEdit(self.centralwidget)
        self.le_chars.setObjectName(_fromUtf8("le_chars"))
        self.verticalLayout.addWidget(self.le_chars)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.le_maxlen = QtGui.QLineEdit(self.centralwidget)
        self.le_maxlen.setObjectName(_fromUtf8("le_maxlen"))
        self.verticalLayout_2.addWidget(self.le_maxlen)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.le_fillchar = QtGui.QLineEdit(self.centralwidget)
        self.le_fillchar.setObjectName(_fromUtf8("le_fillchar"))
        self.verticalLayout_3.addWidget(self.le_fillchar)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("微软雅黑"))
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.lbl_ans = QtGui.QLabel(self.centralwidget)
        self.lbl_ans.setObjectName(_fromUtf8("lbl_ans"))
        self.verticalLayout_5.addWidget(self.lbl_ans)
        self.te_out = QtGui.QTextEdit(self.centralwidget)
        self.te_out.setObjectName(_fromUtf8("te_out"))
        self.verticalLayout_5.addWidget(self.te_out)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.btn_create)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ArtCharMaker", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "输入字符串", None, QtGui.QApplication.UnicodeUTF8))
        self.le_chars.setText(QtGui.QApplication.translate("MainWindow", "Hello!", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "行最大长度", None, QtGui.QApplication.UnicodeUTF8))
        self.le_maxlen.setText(QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "填充字符", None, QtGui.QApplication.UnicodeUTF8))
        self.le_fillchar.setText(QtGui.QApplication.translate("MainWindow", "/wx", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "生成", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_ans.setText(QtGui.QApplication.translate("MainWindow", "结果", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

