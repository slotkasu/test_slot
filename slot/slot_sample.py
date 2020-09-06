import random as rd
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import time


time.sleep(1000)
# 小役の定義
class Koyaku:
	prob = 10000
	payout = 7
	name = ""

	def __init__(self,prob,payout,name):
		self.prob = probToCount(prob)
		self.payout = payout
		self.name = name

	def setProb(self,value):
		self.prob = probToCount(value)
	def getProb(self):
		return self.prob

	def setPayout(self,value):
		self.payout = value
	def getPayout(self):
		return self.payout
	
	def getName(self):
		return self.name

# 全体
class Slot:
	games = 0
	settings = 6
	medals = 0
	x_games = np.zeros(8000,int)
	y_medals = np.zeros(8000,int)

	# 状態
	state = 0
	flag_range = []
	koyaku_list = []

	#フラグの個数を渡すと範囲にして返してくれる
	def countToRange(self,flag_count):
		flag_range = [sum(flag_count[:i]) for i in range(1,len(flag_count)+1)]
		return flag_range

	def __init__(self,koyaku_list):
		self.games = 0
		self.flag_range = self.countToRange([i.getProb() for i in koyaku_list])
		# self.payout = [i.getPayout() for i in koyaku_list]
		self.koyaku_list = koyaku_list
	
	def setState(self,state):
		self.state = state
	def getState(self):
		return self.state
	def getGames(self):
		return self.games
	def getFlagrange(self):
		return self.flag_range

	#抽選
	def lottery(self):
		# 毎回3枚入るので-3
		tama = -3
		ran = rd.randrange(65535)
		for i in range(len(self.getFlagrange())):
			if ran < self.getFlagrange()[i]:
				break

		# 押し順ベルのとき
		if self.koyaku_list[i].getName == "osi_bell":
			if self.getState() == 1 or rd.randrange(6) == 0:
				pass
		if self.koyaku_list[i].getName == "freeze":
			Sleep(10000)

		tama += self.koyaku_list[i].getPayout()

def probToCount(prob):
	return int(65536/prob)

def reset():
	bell = Koyaku(10.7,7,"bell")
	replay = Koyaku(8.11,3,"rep")
	cherry = Koyaku(40,1,"cherry")
	rare_bell = Koyaku(82,7,"rare_bell")
	chance_replay = Koyaku(72.8,3,"chance_rep")
	kyo_cherry = Koyaku(131.6,2,"kyo_cherry")
	chance_me = Koyaku(202.1,1,"chance_me")
	hazure = Koyaku(25.3,0,"hazure")
	freeze = Koyaku(65536,15,"freeze")
	osijun_bell = Koyaku(1.47,7,"osi_bell")

	# 小役たち
	koyaku_tachi = [bell,replay,cherry,rare_bell,chance_replay,kyo_cherry,chance_me,hazure,freeze,osijun_bell]

	slot = Slot(8000,koyaku_tachi)
	return slot


tama = 0


def __main__():
	for i in range(1000000):
		tama += slot.lottery()
		print(tama)