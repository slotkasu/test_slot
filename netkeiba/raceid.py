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

year = '2018'

date = datetime.datetime.now()
#競馬場	開催	日目	レース

course_list = [str(i+8).zfill(2) for i in range(3)]
kaisai_list = [str(i+1).zfill(2) for i in range(4)]
date_list = [str(i+1).zfill(2) for i in range(9)]
race_list = [str(i+1).zfill(2) for i in range(12)]

for course in course_list:
	for kaisai in kaisai_list:
		for date in date_list:
			for race in race_list:
				print(year+course+kaisai+date+race)
				kekka = makeKeibaDataset(year+course+kaisai+date+race)
				if kekka == 3:
					break
				time.sleep(1)

