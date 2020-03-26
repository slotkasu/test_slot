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
from tensorflow.python.client import device_lib

#学習済みNNを解析する　あとで変える

def print_cmx(y_true, y_pred):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
    
    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
    plt.figure(figsize = (12,7))
    sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
    plt.show()

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

X=[]
Y=[]


paths = glob.glob("keiba\\datasets2\\2018\\*")
paths=paths+glob.glob("keiba\\datasets2\\2017\\*")
for path in paths:
    csv_file = open(path, "r", newline="" )
    temp_list = csv.reader(csv_file, delimiter=",")
    flag=0
    for i in temp_list:
        if flag==0:
            flag=1
            continue

        if len(i[5:]) == 172:
            temp_c0=i[5:].count("0")
            if temp_c0 >100:
                continue
            #馬名、着順、オッズ
            Y.append(i[:5])
            X.append(list(map(float,i[5:])))

#3位以内は1、4位以降は0にする
temp=[]
for i in Y:
    if int(i[1])<=3:
        temp.append(0)
    else:
        temp.append(1)
Y=temp

X=np.array(X, dtype="float32")
Y=np.array(Y, dtype="int")

sm = SMOTE(random_state=42)
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
#print_cmx(true_classes, predict_classes)


# model.save("keiba_model.h5",include_optimizer=False)

for i in [0]:
    # weights 結果をplot
    w1 = model.layers[i].get_weights()[0]
    #plt.imshow(w1, cmap='coolwarm', interpolation='nearest')
    # plt.colorbar()
    # plt.figure()
    yoko=[i for i in range(len((w1**2).mean(axis=1)))]
    # plt.plot((w1**2).mean(axis=1), 'o-')
    plt.bar(yoko,(w1**2).mean(axis=1))
    plt.show()

    test=(w1**2).mean(axis=1)
f=open("test.csv","w")
for i in test:
    f.write(str(i)+",")