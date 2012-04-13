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
f_open = open(str(c_id)+'_open_trends.txt', 'w')
f_click = open(str(c_id)+'_click_trends.txt', 'w')
f_pv  = open(str(c_id)+'_pv_trends.txt', 'w')


counter = 0
nodate = 0
#nopurch = 0
#noclick = 0
#noopen = 0
nopv = 0
bad_cl_key = 0
bad_op_key = 0
bad_pv_key = 0




#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}]}):


for item in collection.find({"$and": [{"horizon_month": {"$ne": None}}, {"purchases": {"$ne": None}}, {"signup_time": {"$ne": None}}, {"daily_open": {"$ne": None}}, {"daily_click": {"$ne": None}}]}):

	
	signup_time = item.get('signup_time').date()

        purchases = item.get('purchases')

        for p in range(len(item.get('purchases'))):
		try:
                	days = -(signup_time - item.get('purchases')[p].get('time').date()).days
                	csv.writer(f_purch).writerow([counter, days])
		except Exception:
			nodate += 1


		#CLICKS
		
	click_keys = item.get('daily_click').keys()
 	for key in click_keys:
		try:
             		d = (datetime.strptime(key, '%y%m%d').date() - signup_time).days
			csv.writer(f_click).writerow([counter, d])
			#print d
               	except Exception:
      			bad_cl_key += 1
	
		#OPENS
	open_keys = item.get('daily_open').keys()
 	for key in open_keys:
		try:
               		d = (datetime.strptime(key, '%y%m%d').date() - signup_time).days
			csv.writer(f_open).writerow([counter, d])
				
               	except Exception:
       			bad_op_key += 1
	

		#PAGEVIEWS
		  
		
	pageview_keys = item.get('horizon_month').keys()
       	for key in pageview_keys:
		try:
              		d = (datetime.strptime(key, '%Y%m').date() - signup_time).days
			csv.writer(f_pv).writerow([counter, d])
                except Exception:
              		bad_pv_key += 1










	counter +=1 




#f_purch.close()
f_open.close()
f_click.close()
f_pv.close()




print "counter = " + str(counter)
print  "nodate = " + str(nodate)
#print "nopurch = " + str(nopurch)
#print "noclick = " + str(noclick)
#print "noopen = " + str(noopen)
print "nopv = " + str(nopv)
print "bad_cl_key = " + str(bad_cl_key) 
print "bad_op_key = " + str(bad_op_key)
print "bad_pv_key = " + str(bad_pv_key)


