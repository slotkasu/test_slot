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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from get_race_name import makeRaceName

year = '2020'

date = datetime.datetime.now()
#競馬場	開催	日目	レース

course_list = [str(i+1).zfill(2) for i in range(10)]
kaisai_list = [str(i+1).zfill(2) for i in range(4)]
date_list = [str(i+1).zfill(2) for i in range(9)]
# race_list = [str(i+7).zfill(2) for i in range(6)]
race_list = [str(i+1).zfill(2) for i in range(12)]



options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)
options.add_argument("--log-level=3")

driver = webdriver.Chrome(chrome_options=options)

years=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
for year in years:

	#この番号からはじめる　8桁
	skip = year + "00000000"

	for course in course_list:
		for kaisai in kaisai_list:
			for date in date_list:
				for race in race_list:
					temp = year+course+kaisai+date+race
					print(temp)
					if int(temp) < int(skip):
						continue
					else:
						# original
						# kekka = makeKeibaDataset(year+course+kaisai+date+race,driver=driver)
						#レース名取得
						kekka = makeRaceName(year+course+kaisai+date+race)
						if kekka == 3:
							break