from pymongo import Connection
from datetime import *
import numpy


db = Connection('localhost', 40005)['sailtru']
col = db['profile.1600']

start = datetime.strptime('090111', '%y%m%d').date()
nokeys = 0

for item in col.find({'daily_open': {'$ne:' None}}):
	
	try:
		keys = item['daily_open'].keys()

	except:
		nokeys += 1
	
	if keys:
		for key in keys:
			if datetime.strptime(key, '%y%m%d').date() > start:
				start = datetime.strptime(key, '%y%m%d').date()


print start
print "nokeys = " + str(nokeys)
