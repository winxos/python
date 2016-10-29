import sys
from PyQt4 import QtGui
from Ui_mainform import Ui_MainWindow
from Ui_about import Ui_Dialog
from blumind import *
class wForm(QtGui.QMainWindow):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
	def showAbout(self):
		self.ui.rb3.setChecked(True)
		a=Ui_Dialog()
		a.show()
	def open(self):
		f=QtGui.QFileDialog(self)
		str=""
		if self.ui.rb1.isChecked(): #open bmd files
			file=f.getOpenFileName(self,"选择bmd文件","","Bmd 文件(*.bmd);;All Files(*.*)")
			f=open(file,"r")
			str=f.read()
			f.close()
		if self.ui.rb2.isChecked(): #open folders
			file = f.getExistingDirectory()
			r=[]
			getdir(file,r)
			str="".join(r)
		if self.ui.rb3.isChecked():
			file=f.getOpenFileName(self,"选择dir文件","","dir文件(*.dir)")
			f=open(file,"r")
			str=f.read()
			f.close()
		self.ui.te_dirs.setText(str)
		pass
	def createdirs(self):
		pass
if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	m=wForm()
	m.show()
	sys.exit(app.exec_())


