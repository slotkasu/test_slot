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
from class_fetch import makeKeibaDataset

#urlは手打ちでよろ
#makeKeibaDataset("202006020502")

course_list = ["札幌","函館","福島","新潟","東京","中山","中京","京都","阪神","小倉"]

url = "https://race.netkeiba.com/top/"
html = requests.get(url)
html.encoding =html.apparent_encoding
soup = BeautifulSoup(html.content,'lxml',from_encoding="euc-jp")
course = soup.find_all("th")

ls = []
for i in course:
	if i.text in course_list:
		ls.append(i.text)

print(ls)

course = ls

