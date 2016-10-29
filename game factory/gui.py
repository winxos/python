# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2013)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class form_ui
###########################################################################

class form_ui ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Game Factory", pos = wx.DefaultPosition, size = wx.Size( 960,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.canvas = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer17.Add( self.canvas, 1, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer19.SetMinSize( wx.Size( 100,-1 ) ) 
		self.m_panel12 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel12.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
		self.m_panel12.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
		self.m_panel12.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		gSizer3 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"游戏名称:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.t_name = wx.TextCtrl( self.m_panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.t_name, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"游戏类型:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer3.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.t_type = wx.TextCtrl( self.m_panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.t_type, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"游戏标签:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.t_tag = wx.TextCtrl( self.m_panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.t_tag, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel12.SetSizer( gSizer3 )
		self.m_panel12.Layout()
		gSizer3.Fit( self.m_panel12 )
		bSizer19.Add( self.m_panel12, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_msg = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,120 ), wx.TE_MULTILINE )
		self.m_msg.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer19.Add( self.m_msg, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.t_likes = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.ALIGN_LEFT )
		self.t_likes.Wrap( -1 )
		self.t_likes.SetFont( wx.Font( 16, 74, 90, 90, False, wx.EmptyString ) )
		self.t_likes.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer20.Add( self.t_likes, 0, wx.ALL, 5 )
		
		self.b_likes = wx.Button( self, wx.ID_ANY, u"点赞", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		self.b_likes.SetFont( wx.Font( 16, 74, 90, 90, False, "仿宋" ) )
		self.b_likes.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizer20.Add( self.b_likes, 1, wx.ALL, 5 )
		
		self.b_set = wx.Button( self, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.b_set.SetFont( wx.Font( 16, 74, 90, 90, False, "仿宋" ) )
		self.b_set.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.b_set.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizer20.Add( self.b_set, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer20, 0, wx.EXPAND, 5 )
		
		self.gamelist = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.VSCROLL )
		self.gamelist.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer19.Add( self.gamelist, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer17.Add( bSizer19, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer17 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.t_name.Bind( wx.EVT_TEXT, self.search )
		self.t_type.Bind( wx.EVT_TEXT, self.search )
		self.t_tag.Bind( wx.EVT_TEXT, self.search )
		self.b_likes.Bind( wx.EVT_BUTTON, self.likes )
		self.b_set.Bind( wx.EVT_BUTTON, self.set )
		self.gamelist.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.run_game )
		self.gamelist.Bind( wx.EVT_LIST_ITEM_SELECTED, self.show_msg )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def search( self, event ):
		event.Skip()
	
	
	
	def likes( self, event ):
		event.Skip()
	
	def set( self, event ):
		event.Skip()
	
	def run_game( self, event ):
		event.Skip()
	
	def show_msg( self, event ):
		event.Skip()
	

###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 540,337 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

