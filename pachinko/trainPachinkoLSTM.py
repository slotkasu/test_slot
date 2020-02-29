# -*- coding: utf-8 -*-

from estimate_setting import getSettingList
import numpy as np
import csv

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
    return numpy.array(dataX), numpy.array(dataY)

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
print(dataset)

dataX, dataY=[], []
# for i in range(len(setting))
