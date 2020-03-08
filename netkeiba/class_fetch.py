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

url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=201906020111&rf=shutuba_submenu"


html = requests.get(url)
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.content,'html.parser')

#trタグのHorseListクラスからtr_[0-9]{2}のものだけを抽出
name = soup.find_all("tr",class_="HorseList",id=re.compile('tr_[0-9]+'))

for na in name:	
	divs = na.find_all("div")
	for div in na.find_all("div"):
		print(div.text.strip())
	print("\n_________________________")

# for i in name:
# 	print(i.text)
