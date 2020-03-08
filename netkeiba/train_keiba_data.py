# import tensorflow as tf
import csv
import glob
import numpy as np
from sklearn.model_selection import train_test_split

years=["2019"]
months=["01","02","03","04","05","06","07","08","09","10","11","12"]

X=[]
y=[]

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
            y.append(i[:3])
            #情報
            X.append(i[3:])

y=[1 if int(i[1])<=3 else 0 for i in y]

X=np.array(X, dtype="float32")
y=np.array(y, dtype="int")

#データを全て正規化（0～1）の間に収める
X_min=X.min(axis=0, keepdims=True)
X_max=X.max(axis=0, keepdims=True)
X=(X-X_min) / (X_max - X_min)


#訓練データと試験データ
X_train, X_test, Y_train, Y_test = train_test_split(X, y,train_size=0.8)


exit()

model = tf.keras.Sequential([
    tf.keras.layers.Dense(300, kernel_regularizer=tf.keras.regularizers.l2(0.001), activation=tf.nn.relu, input_dim=len(X.columns)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(300, kernel_regularizer=tf.keras.regularizers.l2(0.001), activation=tf.nn.relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)
])

model.compile(
    loss='binary_crossentropy',
    optimizer=tf.keras.optimizers.Adam(),
    metrics=['accuracy'])

fit = model.fit(train_df,
    train_labels,
    validation_data=(valid_df, valid_labels),
    epochs=30,
    batch_size=32)