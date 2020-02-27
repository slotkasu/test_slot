# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 23:22:57 2019
@author: 1
"""
import sys
import requests
import re
from bs4 import BeautifulSoup
import warnings
import csv
import pprint
import time
import datetime

def getCalendar(i):
	now = datetime.date.today()
	year = now.year
	month = now.month
	day = now.day-1
	#print(year,month,day)
	string = str(year)+str(month).zfill(2)+str(day).zfill(2)
	return string

def skipper(skip_value, daiban):
	for i in skip_value:
		if i in daiban:
			return 1
	return 0

print(skipper(4,14))



print(getCalendar(0))
#print(type(getCalendar(0)))

warnings.simplefilter("ignore")
url = "https://papimo.jp/h/00061833/hit/view/"

for daiban in range(100):
	time.sleep(1)
	html = requests.get(url+str(daiban+1100)+"/"+getCalendar(-1))
	html.encoding = html.apparent_encoding
	soup = BeautifulSoup(html.text)

	title = soup.find("title")
	#- -で囲まれた台の名前を抽出している。
	title = title.get_text().split("-")[1].strip()
	if title == "":
		print("ない")
		continue

	print(str(daiban)+":"+title)

	
	ps = soup.find_all("p",class_="cost")
	if not "２０スロ" in ps[0].string:
		print("いらんやつ")
		continue

	name = soup.find_all("td")
	day="本日"

	cnt=0
	flag=0
	for i in name:
		if cnt == 7:
			break
		if flag == 1:
			#print(i.get_text())
			cnt+=1
		if i.get_text() == day:
			flag=1
			print(day)

