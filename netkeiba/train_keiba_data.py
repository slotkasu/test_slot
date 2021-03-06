import tensorflow as tf
import csv
import glob
import os
import re
import subprocess
import random
import numpy as np
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
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SVMSMOTE, SMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from tensorflow.python.client import device_lib
from statistics import mean, median,variance,stdev
from operator import itemgetter
import pickle
 
def print_cmx(y_true, y_pred):
	labels = sorted(list(set(y_true)))
	cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
	
	df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
	plt.figure(figsize = (12,7))
	sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
	plt.show()

data_create=1

if not os.path.isfile("X_train.txt") or data_create:
	X_train=[]
	Y_train=[]

	count0=[]
	#trainデータを読み込み
	paths = glob.glob("keiba\\datasets2\\2018\\*")
	paths=paths+glob.glob("keiba\\datasets2\\2017\\*")
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
			temp.append(0)
		else:
			temp.append(1)
	Y_train=temp


	X_train=np.array(X_train, dtype="float32")
	Y_train=np.array(Y_train, dtype="int")

	#データを減らす
	# sampler = RandomUnderSampler(random_state=42)
	# X_train, Y_train = sampler.fit_resample(X_train, Y_train)
	# len0 = len([i for i in Y_train if i == 0])
	# len1 = len([i for i in Y_train if i == 1])
	# print(len0,len1)

	#データを増やす
	# sm = SMOTE()
	# se = SMOTEENN(random_state=42)
	# len0 = len([i for i in Y_train if i == 0])
	# len1 = len([i for i in Y_train if i == 1])
	# print(len0,len1)
	# # X_train, Y_train = sm.fit_sample(X_train,Y_train)
	# X_train, Y_train = se.fit_resample(X_train,Y_train)
	# len0 = len([i for i in Y_train if i == 0])
	# len1 = len([i for i in Y_train if i == 1])
	# print(len0,len1)

	#ワンホットベクトルに変えるよ
	Y_train=to_categorical(Y_train)

	#データを全て正規化（0～1）の間に収める
	X_min=X_train.min(axis=0, keepdims=True)
	X_max=X_train.max(axis=0, keepdims=True)
	
	#X_trainとY_trainを保存しておく。
	fx = open('X_train.txt', 'wb')
	fy = open('Y_train.txt', 'wb')
	pickle.dump(X_train, fx)
	pickle.dump(Y_train, fy)

else:
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
model = Sequential()
model.add(Dense(300, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001), input_shape=(X_train.shape[1],),))
model.add(Dropout(0.2))
model.add(Dense(128, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
model.add(Dropout(0.2))
model.add(Dense(Y_train.shape[1], activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
			  optimizer=optimizers.Adam(),
			  metrics=['accuracy'])

epochs=100

history = model.fit(X_train, Y_train,
					batch_size=512,
					epochs=epochs,
					verbose=1,
					validation_data=(X_test, Y_test))

print(history.history.keys())

#学習精度とバリデーションの制度をplot
plt.plot(range(1, epochs+1), history.history['accuracy'], label="training")
plt.plot(range(1, epochs+1), history.history['val_accuracy'], label="validation")
# plt.plot(range(1, epochs+1), history.history['loss'], label="train_loss")
# plt.plot(range(1, epochs+1), history.history['val_loss'], label="valid_loss")
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

score = model.evaluate(X_test, Y_test, verbose=0)

predict_classes = model.predict_classes(X_test)
true_classes = np.argmax(Y_test, 1)
cmx = confusion_matrix(true_classes, predict_classes)
print(cmx)
print_cmx(true_classes, predict_classes)

true_positive = cmx[0][0]/(cmx[0][0]+cmx[0][1])
# print(true_positive)

money=0
atari=0
hazure=0
total=0
atari_list=[]
money_list=[]

for i in range(len(predict_classes)):
	#買うとき
	if predict_classes[i] == 0  and float(odds[i])>2.0:
		money-=100
		# print(test_paths[i])
		#当たった時
		if Y_test[i][0] == float(1):
			# print("あたり"+str(odds[i]))
			money += float(odds[i]) * 100
			atari+=1
			atari_list.append(float(odds[i]))
			money_list.append(money)
		#外れた時
		else:
			# print("はずれ"+str(odds[i]))
			hazure+=1
	total+=1

#あたりと予想した馬で、当たっていた馬のオッズのヒストグラムを表示
plt.hist(atari_list, range=(0, 10));
plt.show()

#所持金の推移
index=[i+1 for i in range(len(money_list))]
plt.plot(index, money_list)
plt.show()

odds_ave= sum(atari_list) / len(atari_list)
print("平均オッズ:"+str(odds_ave))
print("儲け"+str(money))
print(atari, hazure, total)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save("keiba_model.h5",include_optimizer=False)