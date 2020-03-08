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
# name = soup.find_all("td")
# div = name.find_all("div")

name = soup.find_all("tr")

#name = [i for a in soup.find_all("tr") for i in a.find_all("td")]
aaa = []
# for i in name:
	# print(i)
	# print("___________________________________________________")
# for i in name:

for i in name:
	aaa.append(i.find_all("td"))
	

print(aaa)