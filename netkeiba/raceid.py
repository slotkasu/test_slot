import sys
import requests
import re
from bs4 import BeautifulSoup
import csv
import pprint
import time
import datetime
from datetime import timedelta
from class_fetch import makeKeibaDataset

year = '2020'

date = datetime.datetime.now()
#競馬場	開催	日目	レース

course_list = [str(i+1).zfill(2) for i in range(10)]
kaisai_list = [str(i+1).zfill(2) for i in range(4)]
date_list = [str(i+1).zfill(2) for i in range(9)]
# race_list = [str(i+7).zfill(2) for i in range(6)]
race_list = [str(i+1).zfill(2) for i in range(12)]

#この番号からはじめる　8桁

skip = year + "06020811" #"00000000"

for course in course_list:
	for kaisai in kaisai_list:
		for date in date_list:
			for race in race_list:
				temp = year+course+kaisai+date+race
				print(temp)
				if int(temp) < int(skip):
					continue
				else:
					kekka = makeKeibaDataset(year+course+kaisai+date+race)
					if kekka == 3:
						break