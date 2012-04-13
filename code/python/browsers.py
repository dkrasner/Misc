import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")








#########The profile DB#########
con = Connection('localhost', 40006)
#con = Connection('localhost', 40004)
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']


browsers = []

for item in collection.find('browser': {'$exists': True}}):
	for i in range(len(item['browser'].keys())):
		browsers.append(item['browser'].keys()[i])

b = set(browsers)

browser_list = [item for item in b]

browser_count = [0]*len(browser_list) 
	
f = open(str(c_id)+'_browsers.txt', 'w')


noindex = 0
nokeys = 0
for item in collection.find({'browser': {'$exists': True}}):
	try:
		for key in item['browser'].keys():
			try:
				index = browser_list.index(key)
				browser_count[index] += item['browser'][key]
			except Exception:
				noindex += 1

	except Exception:
		nokeys += 1

csv.writer(f).writerow(browser_list)
csv.writer(f).writerow(browser_count)
f.close()


