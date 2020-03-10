import requests
from bs4 import BeautifulSoup

#レース名を引数に番号を返す
def getRaceNum(raceName):
	race=["札幌","函館","福島","新潟","東京","中山","中京","京都","阪神","小倉"]
	#どこかに1を挿入したいので要素を1つ少なくする
	ls = ["0" for i in race]
	ls.pop(0)
	#raceに存在しない競馬場を弾く（香港、ドバイ等）
	if raceName in race:
		#イメージ 
		# 0 0 0 0 0 0 0 0 0
		#　↓
		# 0 0 0 0 1 0 0 0 0 0
		ls.insert(race.index(raceName),"1")
		return ls
	else:
		ls.append("0")
		return ls

#芝ダを引数に番号を返す
def getShibadaNum(shibadaName):
	shibada=["芝","ダ"]
	if shibadaName in shibada:
		return str(shibada.index(shibadaName))
	else:
		return "-1"

#性別を引数に番号を返す
def getSexNum(sexName):
	#getracenumと同じ
	sex=["牡","牝","セ"]
	ls = ["0" for i in sex]
	ls.pop(0)
	if sexName in sex:
		ls.insert(sex.index(sexName),"1")
		return ls
	#不正な値を弾く
	else:
		ls.append("0")
		return ls

#馬場状態を引数に番号を返す
def getStateNum(stateName):
	state=["良","稍","重","不"]
	ls = ["0" for i in state]
	ls.pop(0)
	if stateName in state:
		ls.insert(state.index(stateName),"1")
		return ls
	#不正な値を弾く
	else:
		ls.append("0")
		return ls



#馬名、着順、オッズをリストで返す
def getRaceResult(day):
	url = "https://race.netkeiba.com/race/result.html?race_id="+day+"&rf=race_submenu"
	html = requests.get(url)
	html.encoding = html.apparent_encoding
	soup = BeautifulSoup(html.content,'html.parser')
	name = soup.find_all("tr", class_="HorseList")

	results = []

	for na in name:
		#2重リスト用
		temp = []
		#馬名
		horse = na.find("span", class_="Horse_Name")
		temp.append(horse.text.strip())
		#着順
		rank = na.find("div", class_="Rank")
		temp.append(rank.text.strip())
		#オッズ
		odds = na.find("td", class_="Odds Txt_R")
		temp.append(odds.text.strip())
		#馬番（ソート用）
		umaban = na.find("td", class_="Num Txt_C")
		temp.append(int(umaban.text.strip()))
		results.append(temp)
	

	results.sort(key=lambda x: x[3])#2列めを基準にソート

	#ソートに利用した馬番を削除
	for i in results:
		i.pop(3)

	return results


#2:00.0みたいなやつを秒数にする
def TtoF(time_origin):#stringでください
	ls = time_origin.split(":",1)
	if len(time_origin.split(".")) == 3:
		ls = time_origin.split(".",1)
	if len(ls) == 1:
		return time_origin
	min = float(ls[0])
	sec = float(ls[1])
	tt = min*60 + sec
	return str(tt)