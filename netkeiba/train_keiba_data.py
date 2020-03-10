import tensorflow as tf
import csv
import glob
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

 
def print_cmx(y_true, y_pred):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
    
    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
    plt.figure(figsize = (12,7))
    sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
    plt.show()



years=["2019"]
months=["01","02","03","04","05","06","07","08","09","10","11","12"]

X=[]
Y=[]

for year in years:
    paths = glob.glob("keiba\\datasets\\*")
    for path in paths:
        csv_file = open(path, "r", newline="" )
        temp_list = csv.reader(csv_file, delimiter=",")
        flag=0
        for i in temp_list:
            if flag==0:
                flag=1
                continue
            #馬名、着順、オッズ
            Y.append(i[:3])
            #情報
            X.append(i[3:])

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

model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(X.shape[1],)))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(Y.shape[1], activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True),
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
                    batch_size=32,
                    epochs=30,
                    verbose=1,
                    validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)

predict_classes = model.predict_classes(X_test)
true_classes = np.argmax(Y_test, 1)
cmx = confusion_matrix(true_classes, predict_classes)
print(cmx)
print_cmx(true_classes, predict_classes)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save("keiba_model.h5",include_optimizer=False)