import random as rd
import numpy as np
import matplotlib.pyplot as plt

# 小役の定義
class Koyaku:
	prob = 10000
	payout = 7
	def __init__(self,prob,payout):
		self.prob = probToCount(prob)
		self.payout = payout

	def setProb(self,value):
		self.prob = probToCount(value)
	def getProb(self):
		return self.prob

	def setPayout(self,value):
		self.payout = value
	def getPayout(self):
		return self.payout

# 全体
class Slot:
	games = 0
	settings = 6
	# 状態
	state = True
	flag_range = []
	payout = []

	def __init__(self,games,koyaku_list):
		self.games = 0
		self.flag_range = countToRange([i.getProb() for i in koyaku_list])
		self.payout = [i.getPayout() for i in koyaku_list]
	
	def setState(self,state):
		self.state = state
	def getState(self):
		return self.state
	def getGames(self):
		return self.games
	def getFlagrange(self):
		return self.flag_range
	def getPayout(self):
		return self.payout
	#抽選
	def lottery(self):
		ran = rd.randrange(65535)
		for i in range(len(self.getFlagrange())):
			if ran < self.getFlagrange()[i]:
				# 押し順ベルのとき
				if i == len(self.getFlagrange()) -1:
					if self.getState() == True or rd.randrange(6) == 0:
						pass
					else:
						return -3
				# 毎回3枚入るので-3
				return self.getPayout()[i] - 3
		# print("freeze")
		# Sleep(10000)
		return -3


#フラグの個数を渡すと範囲にして返してくれる
def countToRange(flag_count):
	flag_range = [sum(flag_count[:i]) for i in range(1,len(flag_count)+1)]
	return flag_range

def probToCount(prob):
	return int(65536/prob)


bell = Koyaku(10.7,7)
replay = Koyaku(8.11,3)
cherry = Koyaku(40,1)
rare_bell = Koyaku(82,7)
chance_replay = Koyaku(72.8,3)
kyo_cherry = Koyaku(131.6,2)
chance_me = Koyaku(202.1,1)
osijun_bell = Koyaku(1.47,7)
hazure = Koyaku(18.5,0)

# 小役たち
koyaku_tachi = [bell,replay,cherry,rare_bell,chance_replay,kyo_cherry,chance_me,osijun_bell,hazure]

slot = Slot(8000,koyaku_tachi)



print(slot.getFlagrange())

tama = 0
for i in range(1000000):
	tama += slot.lottery()
print(tama)