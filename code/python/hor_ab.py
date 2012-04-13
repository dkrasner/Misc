import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")
port = raw_input("Enter port: ")



start =  datetime.strptime('120401', '%y%m%d').date()
now = datetime.now().date()




########The profile DB#########
con = Connection('localhost', int(port))
#con = Connection()
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']




#f_purch = open(str(c_id)+'_purch_trends.txt', 'w')
f = open(str(c_id)+'_hor_ab.txt', 'w')


counter = 0


for item in collection.find({"$and": [{"signup_time": {"$ne": None}}, {"daily_open": {"$ne": None}}]}):

	
	signup_time = item.get('signup_time').date()

	if signup_time >= start:
		try:
			op_keys = item['daily_open'].keys()
			last_op = op_keys[len(op_keys)-1]
			op_day = (now - datetime.strptime(last_op, '%y%m%d').date()).days
			if op_day >=3:
				csv.writer(f).writerow(item['_id'])
				counter += 1
	else:
		continue







f.close()

print "counter = " + str(counter)

