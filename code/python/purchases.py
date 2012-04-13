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

 
f = open(str(c_id)+'_purchase_dates.txt', 'w')
g = open(str(c_id)+'_purchase_counts.txt', 'w')

start = datetime.now()

no_st = 0
nodate = 0
noqty = 0
counter = 0
#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"signup_time": {"$exists": True}}]}):
for item in collection.find({"purchases": {"$exists": True}}):
	
	dates = []
	counts = []
   
	ID = item.get('_id')
	dates.append(ID)
	counts.append(ID)
	
	counts.append(0)  #so that purchase dates and counts match up

	try:
		signup_time = item.get('signup_time').date()
		dates.append(signup_time)
	except Exception:
		dates.append('NA')
		no_st +=1 
	
         
	purchases = item.get('purchases')
	for p in range(len(item.get('purchases'))):
		try:
			dates.append(item.get('purchases')[p].get('time').date())
			s = 0
			for q in range(len(item.get('purchases')[p].get('items'))):
				try:
					s += item.get('purchases')[p].get('items')[q].get('qty')
					counts.append(s)
				except Exception:
					noqty += 1
		except Exception:
			nodate += 1
	#print "dates: " + str(dates)
	#print "counts: " + str(counts)
	csv.writer(f).writerow(dates)
	csv.writer(g).writerow(counts)
	counter += 1

f.close()
g.close()


end = datetime.now()  

print 'no_st = ' + str(no_st)
print 'nodate = ' + str(nodate)
print 'noqty = ' + str(noqty)
print (start-end).seconds
print 'counter = ' + str(counter)
