import wx
import numpy as np
import slot_sample

class SlotApp(wx.Frame):

	def __init__(self, parent, id = -1, title = 'Window Title'):
		wx.Frame.__init__(self, parent, id, title)
		self.SetSize((500,200))

		self.panel = wx.Panel(self)

		#フラグ表示用処理
		self.flag_text = wx.StaticText(self.panel,wx.ID_ANY,'小役',style=wx.TE_CENTER)
		font=wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.flag_text.SetFont(font)

		#ボタン作成
		self.startButton=wx.Button(self.panel, label="Start")

		#ボタン割り当て
		self.Bind(wx.EVT_BUTTON, self.startLottery, self.startButton)
		
		#レイアウト設定
		self.layout = wx.BoxSizer(wx.VERTICAL)
		self.layout.Add(self.flag_text,flag=wx.GROW)
		self.layout.Add(self.startButton,flag=wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT, border=10)
		self.panel.SetSizer(self.layout)

		#表示処理
		self.Center()
		self.Show()

	def startLottery(self,event):
		self.flag_text.SetLabel("テスト")
		font=wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.flag_text.SetFont(font)



app=wx.App()
SlotApp(None,id=wx.ID_ANY,title="S牙狼魔戒ノ花XX")
app.MainLoop()