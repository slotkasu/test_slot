#import tensorflow as tf
import csv
import glob

years=["2019"]
months=["01","02","03","04","05","06","07","08","09","10","11","12"]

X=[]
y=[]

for year in years:
    for month in months:
        paths = glob.glob("datasets\\"+year+month+"\\*")
        for path in paths:
            csv_file = open(path, "r", encoding="utf_8", errors="", newline="" )
            temp_list = csv.reader(csv_file, delimiter=",",doublequote=True,lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            for i in temp_list:
                #馬名、着順、オッズ
                y.append(i[:3])

                #情報
                X.append(i[3:])
print(X)
print(y)
exit()

model = tf.keras.Sequential([
    tf.keras.layers.Dense(300, kernel_regularizer=tf.keras.regularizers.l2(0.001), activation=tf.nn.relu, input_dim=len(train_df.columns)),
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