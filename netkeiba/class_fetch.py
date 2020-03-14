import sys
import requests
import re
from bs4 import BeautifulSoup
import warnings
import csv
import pprint
import time
import datetime
from keiba_function import getRaceNum, getSexNum, getShibadaNum, getStateNum, getRaceResult, TtoF
from datetime import timedelta



def makeKeibaDataset(date, train_mode=1):
	url = "https://race.netkeiba.com/race/shutuba_past.html?race_id="+date+"&rf=shutuba_submenu"

	html = requests.get(url)
	html.encoding =html.apparent_encoding
	soup = BeautifulSoup(html.content,'lxml',from_encoding="euc-jp")
	title = soup.find("title").text
	#trタグのHorseListクラスからtr_[0-9]{2}のものだけを抽出
	horseLists = soup.find_all("tr",class_="HorseList",id=re.compile(r"tr_[0-9]+"))
	if len(horseLists) == 0:
		print("サイトが存在しないためスキップします。")
		return 3
	if soup.find("tr",class_="HorseList Cancel"):
		print("除外馬が存在するためスキップします。")
		return 1

	Horseinfo = []#馬情報（前のほうのやつ）
	#テンプレートのtemp
	temp_horse = ["馬名","着順","オッズ","当日芝","当日ダ","当日距離","本日良","本日稍","本日重","本日不","枠番","馬番","中週","体重","体重増減","牡","牝","セ","馬齢","斤量"]
	temp_past = ["札幌","函館","福島","新潟","東京","中山","中京","京都","阪神","小倉","着順","芝","ダ","距離","タイム","良","稍","重","不","頭数","馬番","人気","斤量","通過順1","通過順2","通過順3","通過順4","3ハロン","体重","体重増減","着差"]

	#-------------------------本レースの情報---------------------------
	#racedata01に欲しい物が全部入っています
	baseinfo = soup.find("div",class_ = "RaceData01")
	#appendする用のリストになります
	header = []
	#spanタグに全部あります　全部で3要素です
	data = baseinfo.find("span")
	#芝ダート
	if data.text.strip()[0] == "障":
		return 2
	header = header + getShibadaNum(data.text.strip()[0])
	#距離
	header.append((re.search(r'\d+',data.text).group()))
	# #馬場状態
	temp = baseinfo.find("span", class_ = re.compile(r'Item\d+'))
	header= header + getStateNum(temp.text[-1:])
	
	#######

	for horseList in horseLists:
		# print(horseList)
		temp_info_list = []
		#馬名
		#temp_info_list.append(horseList.find("div", class_="Horse02").get_text().strip())
		#枠番
		temp_info_list.append(horseList.find("td", class_=re.compile(r"Waku\d")).get_text())
		#馬番
		temp_info_list.append(horseList.find("td", class_="Waku").get_text())
		#中n週
		#"中2週"とかの数字だけ抜き出す
		temp = horseList.find("div", class_="Horse06").get_text().strip()
		if re.search(r'\d+', temp):
			temp_info_list.append(re.search(r'\d+', temp).group())
		else:
			temp_info_list.append("0")
		#体重、体重増減
		#体重は484kg(-4)のような形で与えられるので、kgを境に分割
		#増減のほうは括弧を削って格納
		weight = horseList.find("div", class_="Weight").get_text().strip().split("kg")

		if len(weight)==2:
			#体重
			temp_info_list.append(re.search(r'\d+',weight[0]).group())
			#体重増減
			horse_weight_diff=re.findall(r'\((.*)\)',weight[1])[0]
			if re.search(r'\d',horse_weight_diff):
				temp_info_list.append(horse_weight_diff)
			else:
				temp_info_list.append("0")
		#分割出来なかった場合は0を2つ代入
		else:
			temp_info_list.append("0")
			temp_info_list.append("0")

		#性別,馬齢
		#性別、年齢、毛色が1つの要素で取れる ex.牡4芦
		#前から1文字目が性別、2文字目が年齢なので、それを取る
		temp = horseList.find("span", class_="Barei").get_text().strip()
		# print(temp)
		sei, rei = getSexNum(temp[:1]),temp[1:2]
		temp_info_list = temp_info_list + sei
		
		temp_info_list.append(rei)

		#斤量
		#tdタグのjockeyクラスを取る
		#取ってきたやつからspanタグの要素を抽出(2個ある)
		#2個めの要素が斤量なのでそれをもらう
		kin = horseList.find("td", class_="Jockey")
		span = kin.find_all("span")					
		temp_info_list.append(span[1].get_text())
	
		#ここからPast
		temp_past_list=[]
		#PastとRestの情報をhorseListから取得
		pasts=horseList.find_all("td",class_=["Past", "Rest"])
		for past in pasts:
			
			if past.get("class")[0] == "Rest":
				#休養中の例外
				#過去レースの情報数：18個
				for i in range(len(temp_past)):
					temp_past_list.append("0")
				continue

			elif not re.search(r'\d',past.find("div", class_="Data01").find(class_="Num").text):
				#除外された場合
				for i in range(len(temp_past)):
					temp_past_list.append("0")
				continue

			else:
				#競馬場に関する情報
				baba_past=past.find("div",class_="Data01")
				#競馬場
				temp_past_list = temp_past_list + getRaceNum(baba_past.span.text.split(" ")[-1])
				#人気
				temp_past_list.append(baba_past.find(class_="Num").text)
				
				#競馬場の詳細情報
				detail_past=past.find("div",class_="Data05")
				#芝ダ
				if detail_past.text[0] != "障":
					temp_past_list = temp_past_list + getShibadaNum(detail_past.text[0])
				else:
					print(detail_past.text)

					print("GAI")
					return 2
				#距離
				temp_past_list.append(re.search(r'\d+',detail_past.text).group())
				#時間部分だけ取り出す
				time=detail_past.text.split()
				time=time[1]
				#タイム d:dd.dを正規表現で取得
				if re.search(r'[0-9][^0-9][0-9]+\.[0-9]',time):
					temp_past_list.append(TtoF(re.search(r'[0-9][^0-9][0-9]+\.[0-9]',time).group()))
				else:
					temp_past_list.append("0")
				#馬場状態
				temp_past_list = temp_past_list + (getStateNum(detail_past.strong.text))

				#データ03
				data03_past=past.find("div",class_="Data03")
				
				#スペース区切りでsplit
				data03_past=data03_past.text.split()
				#頭数
				temp_past_list.append(re.match(r'([0-9]+)',data03_past[0]).group())
				#馬番
				temp_past_list.append(re.match(r'([0-9]+)',data03_past[1]).group())
				#人気
				if re.search(r'\d+', data03_past[2]):
					temp_past_list.append(re.search(r'([0-9]+)', temp).group())
				else:
					temp_past_list.append("0")
				#斤量
				temp_past_list.append(re.match(r'([0-9]+)',data03_past[4]).group())
				
				#データ06
				data06_past=past.find("div",class_="Data06")
				#スペース区切り
				data06_past=data06_past.text.split()
				
				#通過順がある場合
				if re.search(r'^\d',data06_past[0]):
					#通過順を"-"でスプリット
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

					#通過順の代わりにダミーを作成し、インデックスを保護
					data06_past.insert(0,"0")
				#３ハロン
				temp_past_list.append(re.findall(r'\((.*)\)',data06_past[1])[0])
				if len(data06_past)==3:
					#体重
					temp_past_list.append(re.search(r'\d+',data06_past[2]).group())
					#体重増減
					horse_weight_diff=re.findall(r'\((.*)\)',data06_past[2])[0]
					if re.search(r'\d',horse_weight_diff):
						temp_past_list.append(horse_weight_diff)
					else:
						temp_past_list.append("0")
				
				#体重と体重増減のデータが無い場合の考慮
				#0で埋めておく
				else:
					temp_past_list.append("0")
					temp_past_list.append("0")
				
				#着差用データ
				data07_past_text=past.find("div",class_="Data07").text
				#着差
				temp_past_list.append(re.findall(r'\((.*)\)',data07_past_text)[0])

		#現在と過去の情報を結合させる。
		Horseinfo.append(temp_info_list+temp_past_list)
	
	#レース結果のデータと結合させる。
	RaceInfo=getRaceResult(date)
	
	file_name=""

	#当日の開催なら結果がないので処理を分岐させる
	#もしくは、テストモードで実行している場合は、処理を分岐させる。
	if len(RaceInfo) == 0 or train_mode == 0:
		RaceInfo = Horseinfo
		del temp_horse[:3]

		#結果の代わりにレースの基本情報を入れる
		for i in RaceInfo:
			i.insert(0,header)
		
		file_name='keiba/datasets/'+date+'test.csv'
	else:
		for i in range(len(RaceInfo)):
			RaceInfo[i].extend(header)
			RaceInfo[i].extend(Horseinfo[i])
		#訓練データとして保存
		file_name='keiba/datasets2/'+date[0:4]+"/"+date+'out.csv'
	#print(RaceInfo)
	#csv書き込み
	RaceInfo=[i for i in RaceInfo if not "中止" in i]
	#print(RaceInfo)

	for i in range(5):
		temp_horse.extend(temp_past)

	RaceInfo.insert(0,temp_horse)
	f = open(file_name,'w',newline = "")
	writer = csv.writer(f)
	#print(len(RaceInfo[1]))
	if len(RaceInfo[1]) != 175:
		print("not 175")
	writer.writerows(RaceInfo)
	#print("書き込み完了。お疲れさまでした（朧）")
	return title


makeKeibaDataset("201807010110")