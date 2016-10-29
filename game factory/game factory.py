#-*-coding:utf-8-*-
import gui
import wx
import os,sys
import cache_grab
from sqlite3 import *
datadir="swfdata"
class Form(gui.form_ui):
    def __init__(self,parent=None):
        gui.form_ui.__init__(self,parent)
        self.t_likes.SetLabel("0")
        if wx.Platform == '__WXMSW__':
            from wx.lib.flashwin import FlashWindow
            self.flash = FlashWindow(self, style=wx.SUNKEN_BORDER)
            self.canvas.Add(self.flash,proportion=1, flag=wx.EXPAND,border=5)
        self.conn=connect("wanga_detail.db")
        self.curs=self.conn.cursor()
        self.gamelist.InsertColumn(0, u'序号',width=50)
        w = self.gamelist.GetSizeTuple()[0] #width of listctrl
        self.gamelist.InsertColumn(1, u'游戏名',width=w-75)
        self.gamelist.InsertColumn(2, 'id',width=0)
        self.gamelist.InsertColumn(3, 'src',width=0)
        self.update_list(self.curs.execute('select name,id,src,likes from gamelist'))
    def set(self,event):
        pass
    def update_list(self,ans):
        n=ans.fetchall()
        line=0
        self.gamelist.DeleteAllItems()
        for item in n:
            self.gamelist.InsertStringItem(line,str(line+1))
            self.gamelist.SetStringItem(line,1,item[0])
            self.gamelist.SetStringItem(line,2,str(item[1]))
            self.gamelist.SetStringItem(line,3,item[2])
            line=line+1
    def search(self,event):
        q1='%'+self.t_name.GetValue()+'%'
        q2='%'+self.t_tag.GetValue()+'%'
        q3='%'+self.t_type.GetValue()+'%'
        cmd='select name,id,src,likes from gamelist '\
        'where name like ? and tag like ? and type like ?;'
        self.update_list(self.curs.execute(cmd,(q1,q2,q3)))
    def likes(self,event):
        n=int(self.t_likes.GetLabel())
        self.t_likes.SetLabel("%d"%(n+1))
        pass
    def run_game( self, event ):
        pass

    def show_msg( self, event ):
        n=event.m_itemIndex
        id=self.gamelist.GetItem(n,2).GetText()
        src=self.gamelist.GetItem(n,3).GetText()
        s="id:%s\nsrc:%s"%(id,src)
        self.m_msg.SetValue(s)
        swfname=os.path.basename(s)
        fullname=os.path.join(sys.path[0],datadir,swfname)
        if os.path.exists(fullname):
            src=fullname
            print(src)
        else:
            cache_grab.grab_file(swfname,datadir)
        self.flash.LoadMovie(0, src)

app=wx.App()
f=Form()
f.Show()
app.MainLoop()
