import sys
import requests
import re
from bs4 import BeautifulSoup
import warnings
import csv
import pprint
import time
import datetime
from datetime import timedelta
from results import getResults

year = '2019'

def getRaceID():
    url = "https://race.netkeiba.com/race/result.html?race_id="+day+"&rf=race_submenu"
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.content,'html.parser')
    name = soup.find_all("td")

date = datetime.datetime.now()

month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
cource_list = ['01','02','03','04','05','06','07','08','09','10']
race_list = []
kaisai_list = []
for i in range(12):
    race_list.append(str(i+1))
for i in range(5):
    kaisai_list.append(str(i+1))
    競馬場	開催	日目	レース
for month in month_list:
    for cource in cource_list:
        for kaisai in kaisai_list:
            for race in race_list:
                
