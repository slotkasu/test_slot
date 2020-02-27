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


#list skip_value and int daiban
#return 0 if success
def getSkipper(skip_value, daiban):
	for i in skip_value:
		if str(i) in str(daiban):
			return 1
	return 0


#ls = [4,9]
#for i in range(100):
#	print(i,skipper(ls,i))

print(getCalendar(0))

warnings.simplefilter("ignore")
url = "https://papimo.jp/h/00061833/hit/view/"

data_list=[]

for daiban in range(10):
	daiban+=1
	temp_list=[]
	
	html = requests.get(url+str(daiban+1180)+"/"+getCalendar(-1))
	html.encoding = html.apparent_encoding
	
	soup = BeautifulSoup(html.text)

	ps = soup.find_all("p",class_="cost")
	if len(ps) == 0:
		print("ないです")
		continue
	if not "２０スロ" in ps[0].string:
		print("いらんやつ")
		continue

	title = soup.find("title")
	#- -で囲まれた台の名前を抽出している。
	title = title.get_text().split("-")[1].strip()
	print(str(daiban)+":"+title)

	##tempリストにデータを入力
	#台番をappend
	temp_list.append(str(daiban))

	#機種名をappend
	temp_list.append(title)
	name = soup.find_all("td")
	day="本日"

	cnt=0
	flag=0
	for i in name:
		if cnt == 7:
			break
		if flag == 1:
			#print(i.get_text())
			temp_list.append(i.get_text().strip())
			cnt+=1
		if i.get_text() == day:
			flag=1
			#各項目をappend
			

	data_list.append(temp_list)
	time.sleep(1)

print(data_list)
with open('data/out'+getCalendar(-1)+'.csv','w',newline="") as f:
	writer=csv.writer(f)
	writer.writerows(data_list)

