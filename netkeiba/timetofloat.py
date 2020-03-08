import numpy as np
import re
import csv
import glob

#string time_origin to string tt
def TtoF(time_origin):
	ls = time_origin.split(":",1)
	if len(ls) == 1:
		return time_origin
	min = float(ls[0])
	sec = float(ls[1])
	tt = min*60 + sec
	return str(tt)

def getCsv(filename):#csv wo tottekuru
#16+18+18 kono kankaku
	timeAlt = []
	f = open(filename,"r")
	reader = csv.reader(f)
	for row in reader:
		row[15] = TtoF(row[15])
		row[33] = TtoF(row[33])
		row[51] = TtoF(row[51])
		row[69] = TtoF(row[69])
		row[87] = TtoF(row[87])
		timeAlt.append(row)
	f.close()
	f = open(filename,'w',newline = "")
	writer = csv.writer(f)
	writer.writerows(timeAlt)
	f.close()

paths = glob.glob("keiba\\datasets\\"+"*")

for i in paths:
	getCsv(i)

