import csv
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

bb=50
rb=20
total=rb+bb
total_start=8000

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

total_setting_rate/=np.array(total_setting_rate).sum()

for idx, i in enumerate(total_setting_rate):
	print("設定",str(idx+1),"確率：{:.2%}".format(i))
