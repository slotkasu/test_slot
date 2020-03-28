import tensorflow as tf
import csv
import glob
import os
import re
import subprocess
import numpy as np
import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import optimizers
from keras.utils import to_categorical
from keras.backend.tensorflow_backend import set_session
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from imblearn.over_sampling import SVMSMOTE, SMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from tensorflow.python.client import device_lib
from statistics import mean, median,variance,stdev
import pickle
 
def print_cmx(y_true, y_pred):
	labels = sorted(list(set(y_true)))
	cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
	
	df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
	plt.figure(figsize = (12,7))
	sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
	plt.show()


fx = open('X_train.txt', 'rb')
fy = open('Y_train.txt', 'rb')
X_train=pickle.load(fx)
Y_train=pickle.load(fy)
X_min=X_train.min(axis=0, keepdims=True)
X_max=X_train.max(axis=0, keepdims=True)

X_train=(X_train-X_min) / (X_max - X_min)

X_test=[]
Y_test=[]

test_paths=[]

#testデータを読み込み
paths = glob.glob("keiba\\datasets2\\2019\\*")
for path in paths:
	
	csv_file = open(path, "r", newline="" )
	temp_list = csv.reader(csv_file, delimiter=",")
	flag=0
	for i in temp_list:
		if flag==0:
			flag=1
			continue
		#情報
		if len(i[5:]) == 172:
			if i[5:].count("0") > 100:
				continue
			race_id=path.split("\\")[-1]
			race_id=re.search(r'\d+',race_id).group()
			# print(race_id)
			# print(race_id[6:10])
			# if not race_id[6:10] == "0101":
			# 	continue
			test_paths.append(race_id)
			#馬名、着順、オッズ
			Y_test.append(i[:5])
			X_test.append(list(map(float,i[5:])))

#3位以内は1、4位以降は0にする
temp=[]
for i in Y_test:
	if int(i[1])<=3:
		temp.append(0)
	else:
		temp.append(1)


odds=[i[3] for i in Y_test]
# print(odds)

Y_test=temp

X_test=np.array(X_test, dtype="float32")
Y_test=np.array(Y_test, dtype="int")

print(len(Y_test))
Y_test=to_categorical(Y_test)

# X_min=X_test.min(axis=0, keepdims=True)
# X_max=X_test.max(axis=0, keepdims=True)
X_test=(X_test-X_min) / (X_max - X_min)

for i in device_lib.list_local_devices():
	if i.device_type == "GPU":
		gpus = tf.config.experimental.list_physical_devices('GPU')
		if gpus:
		# Restrict TensorFlow to only allocate 1GB of memory on the first GPU
			try:
				tf.config.experimental.set_virtual_device_configuration(
					gpus[0],
					#GPUの最大使用率を4MBに制限　8GBのままではオーバーフローする。
					[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=512)])
				logical_gpus = tf.config.experimental.list_logical_devices('GPU')
				print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
			except RuntimeError as e:
				# Virtual devices must be set before GPUs have been initialized
				print(e)


#ディープラーニングモデル
model = keras.models.load_model("keiba_model.h5", compile=False)

#NNの出力　0=複勝確率 1＝着外(4着以降)確率
predict=model.predict(X_test)

predict_classes = model.predict_classes(X_test)
true_classes = np.argmax(Y_test, 1)
cmx = confusion_matrix(true_classes, predict_classes)
print(cmx)
# print_cmx(true_classes, predict_classes)

true_positive = cmx[0][0]/(cmx[0][0]+cmx[0][1])
# print(true_positive)

odd_rates=[1,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8]
pred_rates=[0.5,0.6,0.7,0.8,0.9]
# odd_rates=[2.8]
# pred_rates=[0.9]


for pred_rate in pred_rates:
	for odd_rate in odd_rates:
		print(pred_rate,odd_rate)
		money=0
		atari=0
		hazure=0
		total=0
		atari_list=[]
		money_list=[]

		for i in range(len(predict_classes)):
			#買うとき
			if predict_classes[i] == 0  and float(odds[i])>odd_rate and predict[i][0]>pred_rate:
				# print("買い目:"+str(i))
				money-=100
				# print(test_paths[i])
				#当たった時
				if Y_test[i][0] == float(1):
					# print("あたり"+str(odds[i]))
					money += int(float(odds[i]) * 100)
					atari+=1
					atari_list.append(float(odds[i]))
					money_list.append(money)
					# print(money)
				#外れた時
				else:
					# print("はずれ"+str(odds[i]))
					hazure+=1
					# print(money)
			total+=1

		# #あたりと予想した馬で、当たっていた馬のオッズのヒストグラムを表示
		# plt.hist(atari_list, range=(0, 10));
		# plt.show()


		#所持金の推移
		index=[i+1 for i in range(len(money_list))]
		plt.plot(index, money_list)
		plt.show()

		odds_ave= sum(atari_list) / len(atari_list)
		print("平均オッズ:"+str(odds_ave))
		print("儲け"+str(money))
		print(atari, hazure, atari/(atari+hazure))
		total=(atari+hazure)*100
		kaishu=(total+money)/total
		print("回収", kaishu)

