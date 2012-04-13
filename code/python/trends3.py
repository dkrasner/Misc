import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")
port = raw_input("Enter port: ")







########The profile DB#########
con = Connection('localhost', int(port))
#con = Connection()
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']




#f_purch = open(str(c_id)+'_purch_trends.txt', 'w')
f = open(str(c_id)+'_behav_trends.txt', 'w')


counter = 0
bad_hor = 0
nopurch = 0

nohor = 0
noclick = 0
noopen = 0

bad_cl_key = 0
bad_op_key = 0
bad_pur_key = 0




for item in collection.find({"signup_time": {"$ne": None}}).limit(1000):

	
	signup_time = item.get('signup_time').date()

	keys = item.keys()
#	print keys

    ##################

	if 'horizon' in keys:
		hor = 1	
	else:
		hor = 0
		nohor += 1	

   ##################

	if 'daily_click' in keys:
		try:
			cl_keys = item['daily_click'].keys()
			last_cl = cl_keys[len(cl_keys)-1]
			cl_day = (datetime.strptime(last_cl, '%y%m%d').date() - signup_time).days
		except:
			cl_day = -1
  			bad_cl_key += 1
	else:	
		noclick += 1
		cl_day = -10

   ###################

	if 'daily_open'in keys:
		try:
			op_keys = item['daily_open'].keys()
			last_op = op_keys[len(op_keys)-1]
			op_day = (datetime.strptime(last_op, '%y%m%d').date() - signup_time).days
		except:
			op_day = -1
			bad_op_key += 1
	else:
		noopen += 1
		op_day = -10

		
	
   ###################

	if 'purchases' in keys:
		try:	
			pur_len = len(item['purchases'])
			pur_day = (item.get('purchases')[pur_len-1].get('time').date() - signup_time).days
		except:
			pur_day = -1
			bad_pur_key += 1
	else:
		nopurch += 1
		pur_day = -10
    
	
	v = [hor, cl_day, op_day, pur_day] 
	if v == [0, -10, -10, -10] or v == [1, -10, -10, -10]:
		counter += 1
	else:
		csv.writer(f).writerow([hor, cl_day, op_day, pur_day])
		counter +=1 




f.close()



print "counter = " + str(counter)
print "bad_hor = " + str(bad_hor)

print "nopurch = " + str(nopurch)
print "nohor = " + str(nohor)
print "noclick = " + str(noclick)
print "noopen = " + str(noopen)


print "bad_cl_key = " + str(bad_cl_key) 
print "bad_op_key = " + str(bad_op_key)
print "bad_pur_key = " + str(bad_pur_key)

