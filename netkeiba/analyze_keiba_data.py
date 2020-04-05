import csv
import glob
import os
import re
import subprocess
import random
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras import optimizers
from keras.utils import to_categorical
from keras.backend.tensorflow_backend import set_session
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SVMSMOTE, SMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from statistics import mean, median,variance,stdev
from operator import itemgetter
import pickle

#Filter methods
from sklearn.feature_selection import VarianceThreshold
#ランダムフォレスト系
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel

 

#データを再作成する場合は、1にする。
data_create=1

if not os.path.isfile("X_train.txt") or data_create:
	X_train=[]
	Y_train=[]

	count0=[]
	#trainデータを読み込み
	paths=[]
	# years=["2018"]
	years=["2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]
	for i in years:
		paths=paths+glob.glob("keiba\\datasets2\\"+i+"\\*")
	for path in paths:
		#print(path)
		temp_list = []
		with open(path,"r") as f:
			reader = csv.reader(f)
			for row in reader:
				temp_list.append(row)
		
		# csv_file = open(path, "r", newline="" )
		# temp_list = csv.reader(csv_file, delimiter=",")

		temp_list=temp_list[1:]
		temp_list=sorted(temp_list, key=lambda i:int(i[1]))
		temp_list_top3=temp_list[:3]
		temp_list_others=temp_list[3:]

		#3着ではない馬が3頭未満の場合、そのレースは除外
		if len(temp_list_others) < 3:
			continue
		temp_list_others=random.sample(temp_list_others,3)
		temp_list=temp_list_top3+temp_list_others
		for i in temp_list:
			#情報
			if len(i[5:]) == 172:
				temp_c0=i[5:].count("0")
				count0.append(temp_c0)
				#馬名、着順、オッズ
				Y_train.append(i[:5])
				X_train.append(list(map(float,i[5:])))

	m = mean(count0)
	median = median(count0)
	variance = variance(count0)
	stdev = stdev(count0)
	print('平均: {0:.2f}'.format(m))
	print('中央値: {0:.2f}'.format(median))
	print('分散: {0:.2f}'.format(variance))
	print('標準偏差: {0:.2f}'.format(stdev))

	# plt.hist(count0);
	# plt.show()
	# exit()


	#3位以内は1、4位以降は0にする
	temp=[]
	for i in Y_train:
		if int(i[1])<=3:
			temp.append(1)
		else:
			temp.append(0)
	Y_train=temp


	X_train=np.array(X_train, dtype="float32")
	Y_train=np.array(Y_train, dtype="int")


	#ワンホットベクトルに変えるよ
	# Y_train=to_categorical(Y_train)

	#データを全て正規化（0～1）の間に収める
	X_min=X_train.min(axis=0, keepdims=True)
	X_max=X_train.max(axis=0, keepdims=True)
	
	#X_trainとY_trainを保存しておく。
	fx = open('X_train.txt', 'wb')
	fy = open('Y_train_reg.txt', 'wb')
	pickle.dump(X_train, fx)
	pickle.dump(Y_train, fy)

else:
	fx = open('X_train.txt', 'rb')
	fy = open('Y_train_reg.txt', 'rb')
	X_train=pickle.load(fx)
	Y_train=pickle.load(fy)
	X_min=X_train.min(axis=0, keepdims=True)
	X_max=X_train.max(axis=0, keepdims=True)

X_train=(X_train-X_min) / (X_max - X_min)

X_test=[]
Y_test=[]

test_paths=[]
X_race_test=[]
Y_race_test=[]


# #testデータを読み込み
# paths = glob.glob("keiba\\datasets2\\2019\\*")
# for path in paths:
# 	X_race_tmp=[]
# 	Y_race_tmp=[]

# 	csv_file = open(path, "r", newline="" )
# 	temp_list = csv.reader(csv_file, delimiter=",")
# 	flag=0
# 	for i in temp_list:
# 		if flag==0:
# 			flag=1
# 			continue
# 		#情報
# 		if len(i[5:]) == 172:
# 			race_id=path.split("\\")[-1]
# 			race_id=re.search(r'\d+',race_id).group()
# 			# print(race_id)
# 			# print(race_id[6:10])
# 			# if not race_id[6:10] == "0101":
# 			# 	continue
# 			test_paths.append(race_id)
# 			#馬名、着順、オッズ
# 			Y_test.append(i[:5])
# 			X_test.append(list(map(float,i[5:])))

# 			#レースごとにデータを投入するための一時リスト
# 			Y_race_tmp.append(i[:5])
# 			X_race_tmp.append(list(map(float,i[5:])))
	
# 	X_race_test.append(X_race_tmp)
# 	Y_race_test.append(Y_race_tmp)

# odds=[i[3] for i in Y_test]
# # print(odds)

# #3位以内は1、4位以降は0にする
# temp=[]
# for i in Y_test:
# 	if int(i[1])<=3:
# 		temp.append(1)
# 	else:
# 		temp.append(0)


# Y_test=temp

# X_test=np.array(X_test, dtype="float32")
# Y_test=np.array(Y_test, dtype="int")

# Y_test=Y_test.T

# #ワンホットベクトルに変えるよ
# # Y_test=to_categorical(Y_test)

# X_test=(X_test-X_min) / (X_max - X_min)

# sel=VarianceThreshold(threshold=0.01)
# sel.fit(X_train)
# # pandasのまま保持して次の処理を行い場合はこちら

# X_train = sel.transform(X_train)
# X_test = sel.transform(X_test)

X_train = pd.DataFrame(X_train)
Y_train = pd.DataFrame(Y_train)

# print(len(X_train[0]))
# print(sum(sel.get_support()))
# X_vars=np.var(X_train, axis=0)
# vars_list=[]
# for idx, i in enumerate(X_vars):
# 	vars_list.append([idx+1,i])
# vars_list=sorted(vars_list, key=lambda i:i[1])
# print(vars_list)

#testここまで


sel_ = SelectFromModel(RandomForestRegressor(n_estimators=200))
sel_.fit(X_train, Y_train.values.ravel())


rest_features = X_train.columns[sel_.get_support()]
print(len(sel_.get_support()))
print(rest_features+1)