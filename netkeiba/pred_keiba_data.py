import tensorflow as tf
import csv
import glob
import numpy as np
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential, load_model
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
from class_fetch import makeKeibaDataset

 
def print_cmx(y_true, y_pred):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
    
    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
    plt.figure(figsize = (12,7))
    sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
    plt.show()

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        #GPUの最大使用率を4MBに制限　8GBのままではオーバーフローする。
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)


#####################################################################################
#    ここからメイン
#####################################################################################

#レースのurlを入れると予想までやってくれます
##
#札幌 函館 福島 新潟 東京 中山 中京 京都 阪神 小倉
#  01  02   03   04   05  06  07   08   09   10
race_name = 202007010512
race_name =  str(race_name)
title=makeKeibaDataset(race_name)


X=[]
Y=[]
paths = glob.glob("keiba\\datasets\\*out.csv")
for path in paths:
    csv_file = open(path, "r", newline="" )
    temp_list = csv.reader(csv_file, delimiter=",")
    flag=0
    for i in temp_list:
        if flag==0:
            flag=1
            continue

        if len(i[3:]) == 160:
            #馬名、着順、オッズ
            Y.append(i[:3])
            X.append(list(map(float,i[3:])))

temp=[]
for i in Y:
    if int(i[1])<=3:
        temp.append(0)
    else:
        temp.append(1)
Y=temp

X=np.array(X, dtype="float32")
Y=np.array(Y, dtype="int")

sm = SMOTE(random_state=11)
X, Y = sm.fit_sample(X,Y)
Y=to_categorical(Y)

#データを全て正規化（0～1）の間に収める
X_min=X.min(axis=0, keepdims=True)
X_max=X.max(axis=0, keepdims=True)

X_test=[]


paths = glob.glob("keiba\\datasets\\"+race_name+"test.csv")
for path in paths:
    csv_file = open(path, "r", newline="" )
    temp_list = csv.reader(csv_file, delimiter=",")
    flag=0
    for i in temp_list:
        if flag==0:
            flag=1
            continue
        X_test.append(list(map(float,i)))


X_test=np.array(X_test, dtype="float32")


#データを全て正規化（0～1）の間に収める
X_test=(X_test-X_min) / (X_max - X_min)


model = keras.models.load_model("keiba_model.h5", compile=False)

#NNの出力　0=複勝確率 1＝着外(4着以降)確率
predict=model.predict(X_test)

print("--------------------------------------------------------")
print("絶対評価")
#単純なNNの出力
for idx, i in enumerate(predict):
    print(str(idx+1)+"番 複勝確率：{:.3f}".format(i[0]),end=" ")
    print(str(idx+1).zfill(2)+"番 複勝確率：{:.3f}".format(i[0]),"着外確率：{:.3f}".format(i[1]),end=" ")
    if np.argmax(i)==0:
        print("買い")
    else:
        print("不買")

#複勝確率を正規化する。
pred_min=predict.min(axis=0, keepdims=True)
pred_max=predict.max(axis=0, keepdims=True)
predict=(predict-pred_min) / (pred_max - pred_min)

print("--------------------------------------------------------")

uma_ban=[np.array([i]) for i in range(len(predict))]
uma_ban=np.asarray(uma_ban)
predict=predict+uma_ban


print("レース内相対評価")
#レース内で正規化し、相対評価に変更
for i in enumerate(predict):
    print(str(i[0])+"番 複勝確率：{:.3f}".format(i[1][0]),"予想オッズ：{:.3f}".format(1+(1-0.2)/(i[1][0]+0.001)))
for idx, i in enumerate(predict):
    print(str(idx+1).zfill(2)+"番 複勝確率：{:.3f}".format(i[0]),"着外確率：{:.3f}".format(i[1]),"予想オッズ：{:.3f}".format(1+(1-0.2)/(i[0]+0.001)))

print(title)

# predict_classes = model.predict_classes(X_test)
# for idx,i in enumerate(predict_classes):
#     if i == 0:
#         print(str(idx+1)+":買い")
#     if i == 1:
#         print(str(idx+1)+":買うな")

# model.save("keiba_model.h5",include_optimizer=False)