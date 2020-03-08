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

Past=[]

html = requests.get(url)
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.content,'html.parser')

#trタグのHorseListクラスからtr_[0-9]{2}のものだけを抽出
horseLists = soup.find_all("tr",class_="HorseList",id=re.compile(r"tr_[0-9]+"))

Horseinfo = []#馬情報（前のほうのやつ）

for horseList in horseLists:
	temp_info_list = []
	#divs = horseList.find_all("td",class_=)

	#馬名
	temp_info_list.append(horseList.find("div", class_="Horse02").get_text().strip())
	#枠番
	temp_info_list.append(horseList.find("td", class_=re.compile(r"Waku\d")).get_text())
	#馬番
	temp_info_list.append(horseList.find("td", class_="Waku").get_text())
	#中n週
	#"中2週"とかの数字だけ抜き出す
	temp = horseList.find("div", class_="Horse06").get_text().strip()
	temp_info_list.append(re.search(r'\d+', temp).group())
	#体重、体重増減
	#体重は484kg(-4)のような形で与えられるので、kgを境に分割
	#増減のほうは括弧を削って格納
	weight = horseList.find("div", class_="Weight").get_text().strip().split("kg")
	temp_info_list.append(weight[0])
	temp_info_list.append(re.findall(r'\((.*)\)',weight[1])[0])

	#性別,馬齢
	#性別、年齢、毛色が1つの要素で取れる ex.牡4芦
	#前から1文字目が性別、2文字目が年齢なので、それを取る
	temp = horseList.find("span", class_="Barei").get_text().strip()
	sei, rei = temp[:1],temp[1:2]
	temp_info_list.append(sei)
	temp_info_list.append(rei)

	#斤量
	#tdタグのjockeyクラスを取る
	#取ってきたやつからspanタグの要素を抽出(2個ある)
	#2個めの要素が斤量なのでそれをもらう
	kin = horseList.find("td", class_="Jockey")
	span = kin.find_all("span")					
	temp_info_list.append(span[1].get_text())
	
	Horseinfo.append(temp_info_list)

# 	#ここからPast
# 	temp_past_list=[]
# 	pasts=horseList.find_all("td",class_=["Past", "Rest"])
# 	for past in pasts:
		
# 		if past.get("class")[0] == "Rest":
# 			#休養中の例外を後で書く。
# 			continue
# 		else:
# 			#競馬場に関する情報
# 			baba_past=past.find("div",class_="Data01")
# 			#競馬場
# 			temp_past_list.append(baba_past.span.text.split(" ")[-1])
# 			#人気
# 			temp_past_list.append(baba_past.find(class_="Num").text)
			
# 			#競馬場の詳細情報
# 			detail_past=past.find("div",class_="Data05")
# 			#芝ダ
# 			temp_past_list.append(detail_past.text[0])
# 			#距離
# 			temp_past_list.append(re.search(r'\d+',detail_past.text).group())
# 			#タイム d:dd.dを正規表現で取得
# 			temp_past_list.append(re.search(r'[0-9]:[0-9]+\.[0-9]',detail_past.text).group())
# 			#馬場状態
# 			temp_past_list.append(detail_past.strong.text)

# 			#データ03
# 			data03_past=past.find("div",class_="Data03")
# 			data03_past=data03_past.text.split()
# 			# print(data03_past)
# 			#頭数
# 			temp_past_list.append(re.match(r'([0-9]+)',data03_past[0]).group())
# 			#馬番
# 			temp_past_list.append(re.match(r'([0-9]+)',data03_past[1]).group())
# 			#人気
# 			temp_past_list.append(re.match(r'([0-9]+)',data03_past[2]).group())
# 			#斤量
# 			temp_past_list.append(re.match(r'([0-9]+)',data03_past[4]).group())
			
# 			#データ06
# 			data06_past=past.find("div",class_="Data06")
# 			#スペース区切り
# 			data06_past=data06_past.text.split()
# 			#通過順がある場合
# 			if re.match(r'[0-9]-[0-9]',data06_past[0]):
# 				through_past=data06_past[0].split("-")
# 				#通過順を全て入れる
# 				for i in through_past:
# 					temp_past_list.append(i)
# 				#残りを0で埋める
# 				for i in range(4-len(through_past)):
# 					temp_past_list.append("0")
# 			#通過順がない場合
# 			else:
# 				#過去のレースに通過順がなければ全て0にする。
# 				#通過順1
# 				temp_past_list.append("0")
# 				#通過順2
# 				temp_past_list.append("0")
# 				#通過順3
# 				temp_past_list.append("0")
# 				#通過順4
# 				temp_past_list.append("0")
			
# 			#３ハロン
# 			#temp_past_list.append()
# 			#体重
# 			#体重増減
# 			#着差


"""
required information
['1', '1', 'イサチルホープ', '484', '-6', '2', '牡', '7', '55.0']
中を体重の前　馬名を最初に
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