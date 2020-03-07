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
from datetime import timedelta

#取ってくる日付の指定 default = -1
#2日前がほしい→-2　7日前がほしい→-7
calendar_i = -13

def getCalendar(i):
	now = datetime.date.today()-datetime.timedelta(days = -i)
	string_date = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)
	return string_date


#list skip_value and int daiban
#return 0 if success
def getSkipper(skip_value, daiban):
	for i in skip_value:
		if str(i) in str(daiban):
			return 1
	return 0

print(getCalendar(calendar_i))

warnings.simplefilter("ignore")
url = "https://papimo.jp/h/00061833/hit/view/"#gachapon
url = "http://papimo.jp/h/00062026/hit/view/"

data_list=["台番","機種名","BB","RB","BB確率","合成確率","総スタート","最終スタート","最大放出"]

f = open('data/crown_'+getCalendar(calendar_i)+'.csv','w',newline="")
writer = csv.writer(f)
writer.writerow(data_list)
mise_nai_cnt=0
for daiban in range(281,584):#780 1280
	if getSkipper([4,9],daiban):
		print(str(daiban)+":SKIP")
		continue
	
	temp_list=[]
	time.sleep(1)
	html = requests.get(url+str(daiban)+"/"+getCalendar(calendar_i))
	html.encoding = html.apparent_encoding
	
	soup = BeautifulSoup(html.text)

	ps = soup.find_all("p",class_="cost")
	if len(ps) == 0:
		print(str(daiban)+":（店に）ないです。")
		mise_nai_cnt+=1
		if mise_nai_cnt==100:
			break
		continue
	if not "20円" in ps[0].string:#２０スロ
		print(str(daiban)+":（２０スロでは）ないです。")
		mise_nai_cnt=0
		continue

	mise_nai_cnt=0
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
	
	writer.writerow(temp_list)
	

#print(data_list)

f.close()
print("書き込み完了")	

