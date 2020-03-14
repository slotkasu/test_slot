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



X=[]
Y=[]


paths = glob.glob("keiba\\datasets\\*")
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

#3位以内は1、4位以降は0にする
temp=[]
for i in Y:
    if int(i[1])<=3:
        temp.append(0)
    # elif int(i[1])<=6:
    #     temp.append(1)
    # elif int(i[1])<=9:
    #     temp.append(2)
    # elif int(i[1])<=11:
    #     temp.append(3)
    else:
        temp.append(1)
Y=temp


# cnt=0
# t_cnt=0
# for i in Y:
#     t_cnt+=1
#     if i == 3:
#         cnt+=1
# print(cnt,t_cnt)

X=np.array(X, dtype="float32")
Y=np.array(Y, dtype="int")

sm = SMOTE(random_state=11)
X, Y = sm.fit_sample(X,Y)
Y=to_categorical(Y)

#データを全て正規化（0～1）の間に収める
X_min=X.min(axis=0, keepdims=True)
X_max=X.max(axis=0, keepdims=True)
X=(X-X_min) / (X_max - X_min)


#訓練データと試験データ
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,train_size=0.8)

model = keras.models.load_model("keiba_model.h5", compile=False)

predict_classes = model.predict_classes(X_test)
true_classes = np.argmax(Y_test, 1)
cmx = confusion_matrix(true_classes, predict_classes)
print(cmx)
print_cmx(true_classes, predict_classes)


model.save("keiba_model.h5",include_optimizer=False)