#using -*shift-jis*-

from estimate_setting import getSettingList
import numpy as np
import csv

#print(getSettingList(40,35,8000))

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
single_setting = np.argmax(setting, axis=1)+1
print(single_setting)