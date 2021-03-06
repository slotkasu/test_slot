import wx
import numpy as np
from slot_sample import *

#スロットアプリ用クラス
class SlotApp(wx.Frame):

	def __init__(self, parent, id = -1, title = 'Window Title'):
		#抽選中フラグ
		self.onLottery=0

		#スロットクラスを定義
		self.slot=reset()

		#フレームクラスを初期化
		wx.Frame.__init__(self, parent, id, title)
		self.SetSize((800,500))

		#パネルを定義
		self.panel = wx.Panel(self)

		#フラグ表示用処理
		self.flag_text = wx.StaticText(self.panel,wx.ID_ANY,'小役',style=wx.ALIGN_CENTRE_HORIZONTAL |wx.ST_NO_AUTORESIZE)
		self.flag_text2 = wx.StaticText(self.panel,wx.ID_ANY,'',style=wx.ALIGN_CENTRE_HORIZONTAL |wx.ST_NO_AUTORESIZE)
		font=wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.flag_text.SetFont(font)
		self.flag_text2.SetFont(font)

		#ボタン作成
		self.startButton=wx.Button(self.panel, label="Start")

		#ボタン割り当て
		self.Bind(wx.EVT_BUTTON, self.startLottery, self.startButton)
		
		#画像表示
		image = wx.Image('test.jpg')
		self.bitmap = image.ConvertToBitmap()
		self.bitmap = wx.Bitmap(image.Scale(50,50))

		#空の画像
		self.empty_bitmap=wx.EmptyBitmap(50,50,depth=-1) 

		self.lamp=wx.StaticBitmap(self.panel, wx.ID_ANY, self.empty_bitmap,style=wx.ALIGN_CENTRE_HORIZONTAL |wx.ST_NO_AUTORESIZE)
		

		#レイアウト設定
		self.layout = wx.BoxSizer(wx.VERTICAL)
		self.layout.Add(self.flag_text,flag=wx.GROW)
		self.layout.Add(self.flag_text2,flag=wx.GROW)
		self.layout.Add(self.startButton,flag=wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT, border=10)
		self.layout.Add(self.lamp,flag=wx.ALIGN_CENTER)
		self.panel.SetSizer(self.layout)

		#表示処理
		self.Center()
		self.Show()

	def startLottery(self,event):
		if self.onLottery==1:
			return

		if self.slot.getATgames()>0:
			self.lamp.SetBitmap(self.bitmap)
		else:
			self.lamp.SetBitmap(self.empty_bitmap)

		#抽選開始
		self.onLottery=1
		self.slot.lottery()
		self.onLottery=0

		#抽選内容を表示
		self.flag_text.SetLabel(self.slot.getLastflag()+" "+self.slot.getState())
		#累積データを表示
		self.flag_text2.SetLabel(str(self.slot.getGames())+" ATゲーム数:"+str(self.slot.getATgames())+" 持ちメダル:"+str(self.slot.getMedals()))

#アプリ定義
app=wx.App()
#スロットアプリを定義
SlotApp(None,id=wx.ID_ANY,title="S牙狼魔戒ノ花XX")
#アプリ起動
app.MainLoop()