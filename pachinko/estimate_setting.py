import csv
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt


# BB回数、RB回数、合算を入力する
# 戻り値は、設定1から設定6までの確率（設定推測値）
def getSettingList(bb, rb, total_start):
	total=rb+bb
	bonus=[bb,rb,total]
	bonus_name=["bb","rb","total"]
	l=[]

	#設定,BB分母,RB分母,合成分母
	with open('setting/happy.csv') as f:
	    reader = csv.reader(f)
	    l = [row for row in reader]

	#確率密度関数？のリスト
	Y_list=[]


	#BB, RB, 合算ごとに
	for i in range(3):
		temp_Y=[]

		#各設定ごとに	
		for j in range(6):

			#試行回数と生起確率から、確率質量関数？を求めている。
			Y=binom.pmf(range(total_start+1),total_start,1/float(l[j][i+1]))
			Y=Y.tolist()
			temp_Y.append(Y[bonus[i]])

		Y_list.append(temp_Y)

	total_setting_rate=[0 for i in range(6)]

	#BB, RB, 合算ごとに
	for idx, i in enumerate(Y_list):
		#設定1から6
		for jdx, j in enumerate(i):
			tmp_rate=j/sum(i)
			#print(bonus_name[idx],"設定",str(jdx+1),"確率：{:.2%}".format(tmp_rate))
			total_setting_rate[jdx]+=tmp_rate

	#BB, RB, 合算の数値を平均化
	total_setting_rate=[i/sum(total_setting_rate) for i in total_setting_rate]


	for idx, i in enumerate(total_setting_rate):
		#print("設定",str(idx+1),"確率：{:.2%}".format(i))
		continue
	return total_setting_rate

getSettingList(40,35,8000)