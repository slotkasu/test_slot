import tensorflow as tf
import csv
import glob
import os
import subprocess
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
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from tensorflow.python.client import device_lib

 
def print_cmx(y_true, y_pred):
	labels = sorted(list(set(y_true)))
	cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
	
	df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
	plt.figure(figsize = (12,7))
	sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
	plt.show()


X_train=[]
Y_train=[]

#trainデータを読み込み
paths = glob.glob("keiba\\datasets2\\2018\\*")
for path in paths:
	#print(path)
	csv_file = open(path, "r", newline="" )
	temp_list = csv.reader(csv_file, delimiter=",")
	flag=0
	for i in temp_list:
		if flag==0:
			flag=1
			continue
		#情報
		if len(i[3:]) == 172:
			#馬名、着順、オッズ
			Y_train.append(i[:3])
			X_train.append(list(map(float,i[3:])))

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


sm = SMOTE(random_state=11)
X_train, Y_train = sm.fit_sample(X_train,Y_train)
Y_train=to_categorical(Y_train)

#データを全て正規化（0～1）の間に収める
X_min=X_train.min(axis=0, keepdims=True)
X_max=X_train.max(axis=0, keepdims=True)
X=(X-X_min) / (X_max - X_min)

X_test=[]
Y_test=[]


#testデータを読み込み
paths = glob.glob("keiba\\datasets2\\2019\\*")
for path in paths:
	#print(path)
	csv_file = open(path, "r", newline="" )
	temp_list = csv.reader(csv_file, delimiter=",")
	flag=0
	for i in temp_list:
		if flag==0:
			flag=1
			continue
		#情報
		if len(i[3:]) == 172:
			#馬名、着順、オッズ
			Y_test.append(i[:3])
			X_test.append(list(map(float,i[3:])))

#3位以内は1、4位以降は0にする
temp=[]
for i in Y_test:
	if int(i[1])<=3:
		temp.append(0)
	else:
		temp.append(1)
Y_test=temp

X_test=np.array(X_test, dtype="float32")
Y_test=np.array(Y_test, dtype="int")

Y_test=to_categorical(Y_test)

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
model.add(Dense(300, activation='relu', input_shape=(X.shape[1],)))
model.add(Dropout(0.2))
model.add(Dense(300, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(Y.shape[1], activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
			  optimizer=optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True),
			  metrics=['accuracy'])

epochs=1000

history = model.fit(X_train, Y_train,
					batch_size=256,
					epochs=epochs,
					verbose=1,
					validation_data=(X_test, Y_test))

print(history.history.keys())

#学習精度とバリデーションの制度をplot
plt.plot(range(1, epochs+1), history.history['accuracy'], label="training")
plt.plot(range(1, epochs+1), history.history['val_accuracy'], label="validation")
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

print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save("keiba_model.h5",include_optimizer=False)