import csv
import re
import glob

paths = glob.glob("keiba\\datasets2\*\*")

racedata = []
180.145.95.211

for i in paths:
	
	with open(i,"r") as f:
		temp = re.findall("[0-9]+",paths)
		year = temp[1]
		raceid = temp[2]
		temp = csv.reader(f)
		for j in temp:
			racedata.append(j)
	print(racedata)

	exit(1)

馬名,着順,単オッズ,複オッズ小,複オッズ大,当日芝,当日ダ,当日距離,本日良,本日稍,本日重,本日不,枠番,馬番,中週,体重,体重増減,牡,牝,セ,馬齢,斤量,
札幌,函館,福島,新潟,東京,中山,中京,京都,阪神,小倉,着順,芝,ダ,距離,タイム,良,稍,重,不,頭数,馬番,人気,斤量,通過順1,通過順2,通過順3,通過順4,3ハロン,体重,体重増減,着差,
札幌,函館,福島,新潟,東京,中山,中京,京都,阪神,小倉,着順,芝,ダ,距離,タイム,良,稍,重,不,頭数,馬番,人気,斤量,通過順1,通過順2,通過順3,通過順4,3ハロン,体重,体重増減,着差,
札幌,函館,福島,新潟,東京,中山,中京,京都,阪神,小倉,着順,芝,ダ,距離,タイム,良,稍,重,不,頭数,馬番,人気,斤量,通過順1,通過順2,通過順3,通過順4,3ハロン,体重,体重増減,着差,
札幌,函館,福島,新潟,東京,中山,中京,京都,阪神,小倉,着順,芝,ダ,距離,タイム,良,稍,重,不,頭数,馬番,人気,斤量,通過順1,通過順2,通過順3,通過順4,3ハロン,体重,体重増減,着差,
札幌,函館,福島,新潟,東京,中山,中京,京都,阪神,小倉,着順,芝,ダ,距離,タイム,良,稍,重,不,頭数,馬番,人気,斤量,通過順1,通過順2,通過順3,通過順4,3ハロン,体重,体重増減,着差
'year', 'race_number', 'dirt', 'turf', 'distance', 'waku', 'uma_ban', 'naka', 'weight', 'weight_diff', 'sex', 'old', 'kinryo',
'cource1', 'rank1', 'turf1', 'dirt1', 'distance1', 'time1', 'baba1', 'shusso1', 'uma_ban1', 'ninki1', 'kinryo1', 'pass1_1', 'pass2_1', 'pass3_1', 'pass4_1', 'fualong1', 'weight1', 'weight_diff1', 'chakusa1',
'cource2', 'rank2', 'turf2', 'dirt2', 'distance2', 'time2', 'baba2', 'shusso2', 'uma_ban2', 'ninki2', 'kinryo2', 'pass1_2', 'pass2_2', 'pass3_2', 'pass4_2', 'fualong2', 'weight2', 'weight_diff2', 'chakusa2',
'cource3', 'rank3', 'turf3', 'dirt3', 'distance3', 'time3', 'baba3', 'shusso3', 'uma_ban3', 'ninki3', 'kinryo3', 'pass1_3', 'pass2_3', 'pass3_3', 'pass4_3', 'fualong3', 'weight3', 'weight_diff3', 'chakusa3',
'cource4', 'rank4', 'turf4', 'dirt4', 'distance4', 'time4', 'baba4', 'shusso4', 'uma_ban4', 'ninki4', 'kinryo4', 'pass1_4', 'pass2_4', 'pass3_4', 'pass4_4', 'fualong4', 'weight4', 'weight_diff4', 'chakusa4',
'cource5', 'rank5', 'turf5', 'dirt5', 'distance5', 'time5', 'baba5', 'shusso5', 'uma_ban5', 'ninki5', 'kinryo5', 'pass1_5', 'pass2_5', 'pass3_5', 'pass4_5', 'fualong5', 'weight5', 'weight_diff5', 'chakusa5'