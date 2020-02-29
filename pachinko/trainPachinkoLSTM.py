# -*- coding: utf-8 -*-

from estimate_setting import getSettingList
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


#print(getSettingList(40,35,8000))

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        xset = []
        for j in range(dataset.shape[1]):
            a = dataset[i:(i+look_back), j]
            xset.append(a)
        dataY.append(dataset[i + look_back, 0])
        dataX.append(xset)
    return np.array(dataX), np.array(dataY)

#データ読み込み
with open('data/feb.csv') as f:
    reader = csv.reader(f)
    data = [row for row in reader]

#360番で実験　別にどれでもいい
data360 = [i for i in data if i[0] == "366"]

#BB RB TotalGames
setting=[getSettingList(int(i[2]),int(i[3]),int(i[1])) for i in data360]

setting = np.array(setting,dtype='float32')

#0～5なので、設定値の1～6に変更する。
single_setting =np.array(np.argmax(setting, axis=1)+1)
single_setting = single_setting.reshape([len(setting),1])

print(single_setting.shape)
print(setting.shape)
dataset=np.concatenate([single_setting, setting],1)

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))

dataset=create_dataset(dataset, 30)
print(dataset)

dataX, dataY=[], []
# for i in range(len(setting))
