import sys,os
from PyQt4 import QtGui
from calcer import Ui_Form
from userfunction import *
class wForm(QtGui.QMainWindow):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui=Ui_Form()
		self.ui.setupUi(self)
	def calc(self):
		v=self.ui.txt.toPlainText()
		self.ui.txtout.setPlainText(str(eval(v)))
if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	m=wForm()
	m.show()
	sys.exit(app.exec_())


