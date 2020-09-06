import random as rd
import numpy as np
import matplotlib.pyplot as plt
import time

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
	x_games = np.arange(0,10000)
	y_medals = np.zeros(10000)
	last_flag = ""

	# 状態
	state = 0
	AT_games_left = 0
	flag_range = []
	koyaku_list = []

	maki_count = 0

	def AT_games_won(self,mode):
		ran = rd.randrange(100)
		if mode == 0:
			if ran < 70:
				return 50
			elif ran > 97:
				return 100
			else:
				return 70
		elif mode == 1:
			if ran < 70:
				return 100
			elif ran < 80:
				return 150
			else:
				return 50
		elif mode == 2:
			if ran <= 50:
				return 500
			else:
				return 200

	#AT抽選
	def AT_lottery(self,flag):
		ran = rd.randrange(100)
		if flag == "chance_rep":
			if ran < 60:
				self.state = 1
				self.AT_games_left += self.AT_games_won(0)
			elif ran < 80 and self.state != 0:
				self.AT_games_left += self.AT_games_won(1)
		elif flag == "kyo_cherry":
			if ran < 20:
				self.state = 1
				self.AT_games_left += 50
			elif ran < 30 and self.state != 0:
				self.AT_games_left += self.AT_games_won(1)

	#フラグの個数を渡すと範囲にして返してくれる
	def countToRange(self,flag_count):
		flag_range = [sum(flag_count[:i]) for i in range(1,len(flag_count)+1)]
		return flag_range

	def __init__(self,koyaku_list):
		self.games = 0
		self.AT_games_left = 0
		self.flag_range = self.countToRange([i.getProb() for i in koyaku_list])
		# self.payout = [i.getPayout() for i in koyaku_list]
		self.koyaku_list = koyaku_list

	def getMedals(self):
		return self.medals

	def setState(self,state):
		self.state = state
	def getState(self):
		if self.state == 0:
			return "通常"
		elif self.state == 1:
			return "AT"
	def getGames(self):
		return self.games
	def getFlagrange(self):
		return self.flag_range
	def getATgames(self):
		return self.AT_games_left


	def getLastflag(self):
		return self.last_flag

	#抽選
	def lottery(self):
		
		if self.AT_games_left == 0:
			self.state = 0

		ran = rd.randrange(65535)
		for i in range(len(self.getFlagrange())):
			if ran < self.getFlagrange()[i]:
				break
		
		# makimono
		if self.koyaku_list[i].getName() == "chance_rep":
			self.maki_count += 1
			if ran%2 == 1:
				self.AT_lottery("chance_rep")
			else:
				self.AT_games_won(0)
		# 今日チェ
		elif self.koyaku_list[i].getName() == "kyo_cherry":
			if ran % 3 == 0:
				self.AT_lottery("kyo_cherry")
			if self.state != 0:
				self.AT_games_won(0)

		# 押し順ベルのとき
		elif self.koyaku_list[i].getName() == "osi_bell":

			if self.state == 1 or rd.randrange(6) == 0:
				pass
			else:
				self.medals -= self.koyaku_list[i].getPayout()
		elif self.koyaku_list[i].getName() == "freeze":
			print("freeze")
			self.AT_games_won(2)
			# time.sleep(10)
			#曲を流す

		# 毎回3枚入るので-3
		self.medals += self.koyaku_list[i].getPayout() -3

		self.y_medals[self.games] = self.medals
		if self.state != 0:
			self.AT_games_left -= 1
		self.games += 1
		self.last_flag = self.koyaku_list[i].getName()

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

	slot = Slot(koyaku_tachi)
	return slot


tama = 0


def __main__():
	slot = reset()
	for i in range(10000):
		slot.lottery()
	print(slot.getMedals())

	plt.plot(slot.x_games,slot.y_medals)
	plt.show()
