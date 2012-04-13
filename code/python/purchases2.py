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




f_purch = open(str(c_id)+'_purchases.txt', 'w')

counter = 0
badrecord = 0



#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}]}):


for item in collection.find({"$and": [{"purchases": {"$ne": None}}, {"signup_time": {"$ne": None}}]}):

	
	ID = item.get('_id')
	
	signup_time = item.get('signup_time')

        purchases = item.get('purchases')

        for p in range(len(item.get('purchases'))):
		try:
                	date = item.get('purchases')[p].get('time')
			price = item.get('purchases')[p].get('price')
			qty = item.get('purchases')[p].get('qty')
                	csv.writer(f_purch).writerow([ID, signup_time, date, price, qty])
		except Exception:
			badrecord += 1


	counter +=1 




f_purch.close()



print "counter = " + str(counter)
print  "badrecord = " + str(badrecord)
#print "nopurch = " + str(nopurch)

