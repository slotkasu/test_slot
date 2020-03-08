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
horseLists = soup.find_all("tr",class_="HorseList",id=re.compile('tr_[0-9]+'))

Horseinfo = []#馬情報（前のほうのやつ）

for horseList in horseLists:
	temp_info_list = []
	#divs = horseList.find_all("td",class_=)
	#枠番
	temp_info_list.append(horseList.find("td", class_=re.compile("Waku\d")).get_text())
	#馬番
	temp_info_list.append(horseList.find("td", class_="Waku").get_text())
	#temp = horseList.find("td", class_="Horse_Info")
	#馬名
	temp_info_list.append(horseList.find("div", class_="Horse02").get_text().strip())
	#
	weight = horseList.find("div", class_="Weight").get_text().strip().split("kg")
	temp_info_list.append(weight[0])
	temp_info_list.append(re.findall(r'\((.*)\)',weight[1])[0])
	#中n週
	temp = horseList.find("div", class_="Horse06").get_text().strip()
	temp_info_list.append(re.search(r'\d+', temp).group())
	#性別,馬齢
	temp = horseList.find("span", class_="Barei").get_text().strip()
	sei, rei = temp[:1],temp[1:2]
	temp_info_list.append(sei)
	temp_info_list.append(rei)


	#斤量
	temp = horseList.find_all("span")
	print(temp)
	Horseinfo.append(temp_info_list)
	
	
	#print("\n_________________________")


	#ここからPast
#print(Horseinfo)
for i in Horseinfo:
	print(i)



	

"""
required information

馬名 -Horse02
着順 --別ページ　別関数から取得
オッズ　--同上
枠 --Waku1
馬番 --Waku
中週 --Horse06
体重 --Weight[0]
体重増減 --Weight[1]
性別 
馬齢
斤量

4つ分↓
競馬場
人気
芝ダ
距離
タイム
馬場状態
頭数
馬番
人気
斤量
通過順１
2
3
4
上がり3ハロン
体重
体重増減
着差

#競馬場の名前を数値化
def getCourseName(course):
	if course == "":
	elif course == "":
	elif course == "":
	elif course == "":
	elif course == "":
	elif course == "":
	elif course == "":
	elif course == "":
	elif course == "":
	elif course == "":


"""