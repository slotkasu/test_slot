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
horseLists = soup.find_all("tr",class_="HorseList",id=re.compile('tr_[0-9]+'))

for horseList in horseLists:	
	
	#divs = horseList.find_all("td",class_=)
	print("\n_________________________")

	#ここからPast
	temp_past_list=[]
	pasts=horseList.find_all("td",class_=["Past", "Rest"])
	for past in pasts:
		
		if past.get("class")[0] == "Rest":
			#休養中の例外を後で書く。
			continue
		else:
			#競馬場に関する情報
			baba_past=past.find("div",class_="Data01")
			#競馬場
			temp_past_list.append(baba_past.span.text.split(" ")[-1])
			#人気
			temp_past_list.append(baba_past.find(class_="Num").text)
			
			#競馬場の詳細情報
			detail_past=past.find("div",class_="Data05")
			#芝ダ
			temp_past_list.append(detail_past.text[0])
			#距離
			temp_past_list.append(re.search(r'\d+',detail_past.text).group())
			#タイム d:dd.dを正規表現で取得
			temp_past_list.append(re.search(r'[0-9]:[0-9]+\.[0-9]',detail_past.text).group())
			#馬場状態
			temp_past_list.append(detail_past.strong.text)

			#データ03
			data03_past=past.find("div",class_="Data03")
			data03_past=data03_past.text.split()
			# print(data03_past)
			#頭数
			temp_past_list.append(re.match(r'([0-9]+)',data03_past[0]).group())
			#馬番
			temp_past_list.append(re.match(r'([0-9]+)',data03_past[1]).group())
			#人気
			temp_past_list.append(re.match(r'([0-9]+)',data03_past[2]).group())
			#斤量
			temp_past_list.append(re.match(r'([0-9]+)',data03_past[4]).group())
			
			#データ06
			data06_past=past.find("div",class_="Data06")
			#スペース区切り
			data06_past=data06_past.text.split()
			#通過順がある場合
			if re.match(r'[0-9]-[0-9]',data06_past[0]):
				through_past=data06_past[0].split("-")
				#通過順を全て入れる
				for i in through_past:
					temp_past_list.append(i)
				#残りを0で埋める
				for i in range(4-len(through_past)):
					temp_past_list.append("0")
			#通過順がない場合
			else:
				#過去のレースに通過順がなければ全て0にする。
				#通過順1
				temp_past_list.append("0")
				#通過順2
				temp_past_list.append("0")
				#通過順3
				temp_past_list.append("0")
				#通過順4
				temp_past_list.append("0")
			
			#３ハロン
			temp_past_list.append()
			#体重
			#体重増減
			#着差


	print(len(temp_past_list))





# for i in name:
# 	print(i.text)
