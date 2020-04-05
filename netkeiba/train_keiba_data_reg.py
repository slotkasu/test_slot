import tensorflow as tf
import csv
import glob
import os
import re
import subprocess
import random
import numpy as np
import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras import optimizers
from keras.utils import to_categorical
from keras.backend.tensorflow_backend import set_session
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SVMSMOTE, SMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from tensorflow.python.client import device_lib
from statistics import mean, median,variance,stdev
from operator import itemgetter
import pickle


#trainデータを読み込み
paths=[]
years=["2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]
importrant=[3,8,9,10,11,12,17,28,32,37,38,40,41,42,43,45,46,47,48,59,63,68,69,72,73,76,77,78,79,90,94,99,100,103,104,107,108,109,110,121,125,131,134,138,139,140,141,152,156,162,169,170,171,172]

for i in years:
	paths=paths+glob.glob("keiba\\datasets2\\"+i+"\\*")
for path in paths:
	#print(path)
	temp_list = []
	with open(path,"r") as f:
		reader = csv.reader(f)
		for row in reader:
			print(row[important])
			temp_list.append(row)
