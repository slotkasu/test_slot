import requests
from bs4 import BeautifulSoup

#レース名を引数に番号を返す
def getRaceNum(raceName):
    race=["札幌","函館","福島","新潟","東京","中山","中京","京都","阪神","小倉"]
    if raceName in race:
        return str(race.index(raceName)+1)
    else:
        return "-1"

#芝ダを引数に番号を返す
def getShibadaNum(shibadaName):
    shibada=["芝","ダ"]
    if shibadaName in shibada:
        return str(shibada.index(shibadaName))
    else:
        return "-1"

#性別を引数に番号を返す
def getSexNum(sexName):
    sex=["牡","牝","セ"]
    if sexName in sex:
        return str(sex.index(sexName))
    else:
        return "-1"

#馬場状態を引数に番号を返す
def getStateNum(stateName):
    state=["良","稍","重","不"]
    if stateName in state:
        return str(state.index(stateName))
    else:
        return "-1"



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
        #オッズ
        odds = na.find("td", class_="Odds Txt_R")
        temp.append(odds.text.strip())
        #着順
        rank = na.find("div", class_="Rank")
        temp.append(rank.text.strip())
        #馬番（ソート用）
        umaban = na.find("td", class_="Num Txt_C")
        temp.append(int(umaban.text.strip()))
        results.append(temp)
    

    results.sort(key=lambda x: x[3])#2列めを基準にソート

    for i in results:
        i.pop(3)

    for i in results:
        print(i)
    return results