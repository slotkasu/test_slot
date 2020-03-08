

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



