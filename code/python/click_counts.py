import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv
import simplejson as json



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")
port = raw_input("Enter port: ")


f = open(str(c_id)+'_click_counts_03-25-12.txt', 'w')


########The profile DB#########
con = Connection('localhost', int(port))
#con = Connection()
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']



now = datetime.strptime('120325', '%y%m%d').date()

counter = 0
badkey = 0

for item in collection.find({"daily_click": {"$ne": None}}):
	
	ID = item.get('_id')

	clicks = 0
			
	try:
		keys = item['daily_click'].keys()
		for key in keys:
			date_diff = (now - datetime.strptime(key, '%y%m%d').date()).days
         		if (float(date_diff)/7 <= 1):
				clicks += item['daily_click'][key]
		
	except:
		badkey += 0							
             
	csv.writer(f).writerow([ID, clicks])

					



f.close()

print "counter: " + str(counter)
print "badkey: " + str(badkey)
	




