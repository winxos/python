import sys,os
from PyQt4 import QtGui
from form import Ui_wForm
class wForm(QtGui.QMainWindow):

	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui=Ui_wForm()
		self.ui.setupUi(self)
	def getSuffix(self,n):
		r=n.rfind('.')
		return r+1
	def isProeFile(self,x):
		if x[self.getSuffix(x):].isdigit():
			return 1
		print(x,"is not proe file!")
		return 0
	def openPath(self):
		f=QtGui.QFileDialog(self)
		file = f.getExistingDirectory()
		self.ui.txtmsg.clear()
		os.chdir(file)
		for x in os.listdir(file):
			if self.isProeFile(x)==1 and os.path.isfile(x):
				self.ui.txtmsg.appendPlainText(x)
	def reVersion(self):
		def fun(x):
			ax=''
			r=self.getSuffix(x)
			ax=x[:r]+'1'
			return ax
		s=self.ui.txtmsg.toPlainText()
		for x in s.split():
			self.ui.txtout.append(fun(x))
	def purge(self):
		rdict={}
		rlist=[]
		def pur(n):
			r=self.getSuffix(x)
			i=int(n[r:])
			if n[:r] in rdict:
				if rdict[n[:r]]<i:
					rlist.append(n[:r]+str(rdict[n[:r]]))
					rdict[n[:r]]=i
			else:
				rdict[n[:r]]=int(n[r:])
		s=self.ui.txtmsg.toPlainText()
		for x in s.split():
			pur(x)
		for x in rlist:
			self.ui.txtout.append("del "+x)
			os.remove(x)
		for r,i in rdict.items():
			if i>1:os.rename(r+"%s"%i,r+'1')
		self.ui.txtout.append("Done!")

if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	m=wForm()
	m.show()
	sys.exit(app.exec_())
