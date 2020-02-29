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

warnings.simplefilter("ignore")
url = "http://swallow.5ch.net/livejupiter/subback.html"
#url = "http://papimo.jp/h/00062026/hit/view/373/20200227"

def thread_and_res(string):#スレッド名とレス数を返す
    #print(string) #test
    #頭3つの文字列だけのやつを切り捨てる
    if len(string.split(" ",1)) == 1:
        return None
    number = 0
    title = string.split(" ",1)[1]#スレ順を切り捨てる
    
    if title[-3] == '(':#レス数の桁が違うと文字列が切り取れない不具合があったのでレス数を判定
        title,number = title[:-3],title[-3:]#スレタイとレス数に分割する
    elif title[-4] == '(':
        title,number = title[:-4],title[-4:]#スレタイとレス数に分割する
    elif title[-5] == '(':
        title,number = title[:-5],title[-5:]#スレタイとレス数に分割する
    else 
        break
    number = re.findall("\((.*)\)",number)#レス数を数字にする
    
    #return title.encode('unicode-escape'), number[0].encode('unicode-escape')
    return title.strip(), number[0]
    #return ascii(title), ascii(number[0])


def __init__():
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text)
    name = soup.find_all("a")
    with open('./sample.csv','a', errors="ignore") as f:
        writer = csv.writer(f)

        for na in name:
            temp = na.get_text()
            temp=thread_and_res(temp)#分割

            if temp != None:#分割に失敗していなければ↓
                if "5ちゃんねるへようこそ" in temp:#下の方の邪魔なやつが来たら終わる
                    break
                print(temp[0], temp[1])
                f.write(temp[0]+","+temp[1]+"\n")
                #writer.writerow(temp[0]+","+temp[1])

while True:
    __init__()
    time.sleep(60)