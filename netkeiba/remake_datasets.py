import csv
import glob
import os
import re
import subprocess
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SVMSMOTE, SMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from statistics import mean, median,variance,stdev
from operator import itemgetter
import pickle


#trainデータを読み込み
paths=[]
# years=["2020","2019","2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]
years=["2018"]
important=[2,7,8,9,10,11,16,27,31,36,37,39,40,41,42,44,45,46,47,58,62,67,68,71,72,75,76,77,78,89,93,98,99,102,103,106,107,108,109,120,124,130,133,137,138,139,140,151,155,161,168,169,170,171]


for i in years:
	paths=paths+glob.glob("keiba\\datasets2\\"+i+"\\*")

for proc, path in enumerate(paths):
	if proc % 1000 == 0:
		print(proc)
	#print(path)
	temp_list = []
	flag177=1
	with open(path,"r") as f:
		reader = csv.reader(f)
		
		for row in reader:
			#旧バージョンのラベル＋特徴量の数でないものを晒す
			if len(row)!=177:
				print("skip "+path.split("\\")[-1])
				flag177=0
				continue
			#ラベル部分　オッズとか
			row_pre=row[:5]
			#それ以外
			row_past=row[5:]
			#ランダムフォレストのやつでええ感じと判断された特徴量たち
			row_past = [i for idx, i in enumerate(row_past) if idx in important]
			row=row_pre+row_past
			temp_list.append(row)

	#新しいディレクトリ、outを消す
	new_path=path.replace("datasets2","datasets3")
	new_path=new_path.replace("out","")

	#csvを作る
	if flag177 == 1:
		with open(new_path, "w", newline="") as f:
			writer = csv.writer(f)
			writer.writerows(temp_list)
