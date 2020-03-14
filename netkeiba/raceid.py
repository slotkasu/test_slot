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

year = '2019'

def getRaceID():
    url = "https://race.netkeiba.com/race/result.html?race_id="+day+"&rf=race_submenu"
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.content,'html.parser')
    name = soup.find_all("td")

date = datetime.datetime.now()
#競馬場	開催	日目	レース

course_list = [str(i+1).zfill(2) for i in range(10)]
kaisai_list = [str(i+1).zfill(2) for i in range(4)]
date_list = [str(i+1).zfill(2) for i in range(9)]
race_list = [str(i+1).zfill(2) for i in range(12)]

for course in course_list:
    for kaisai in kaisai_list:
        for date in date_list:
            for race in race_list:
                print(year+course+kaisai+date+race)
				
                kekka = makeKeibaDataset(year+course+kaisai+date+race)
                if kekka == -1:
                    break

                time.sleep(1)

