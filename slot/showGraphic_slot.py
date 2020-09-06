import wx
import numpy as np

class SlotApp(wx.Frame):
	def __init__(self, parent, id = -1, title = 'Window Title'):
		wx.Frame.__init__(self, parent, id, title)
		self.SetSize((500,200))

		panel = wx.Panel(self)

		#フラグ表示用処理
		self.flag_text = wx.StaticText(panel,wx.ID_ANY,'S牙狼～Type-A～',style=wx.TE_CENTER)
		font=wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.flag_text.SetFont(font)

		#ボタン作成
		self.startButton=wx.Button(panel, label="Start")

		#ボタン割り当て
		self.Bind(wx.EVT_BUTTON)
		
		#レイアウト設定
		layout = wx.BoxSizer(wx.VERTICAL)
		layout.Add(self.flag_text,flag=wx.GROW)
		layout.Add(self.startButton,flag=wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT, border=10)

		panel.SetSizer(layout)

		self.Center()
		self.Show()
		

app=wx.App()
SlotApp(None,id=wx.ID_ANY,title="スロットくん")
app.MainLoop()