import sys
from PyQt4 import QtGui
from Ui_ArtCharMaker import Ui_MainWindow
from ArtCore import *
class wForm(QtGui.QMainWindow):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
	def btn_create(self):
		s_in=self.ui.le_chars.text()
		i_maxlen=int(self.ui.le_maxlen.text())
		s_fill=self.ui.le_fillchar.text()
		#self.ui.te_out.setText("%s%d%s"%(s_in,i_maxlen,s_fill))
		self.ui.te_out.setText("%s"%convertStr(s_in,f=s_fill))
		cb=QtGui.QApplication.clipboard()
		cb.setText(self.ui.te_out.toPlainText())
		self.ui.lbl_ans.setText("结果已经复制到剪贴板！")
		pass
if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	m=wForm()
	m.show()
	sys.exit(app.exec_())
