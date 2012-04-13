import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv
import simplejson as json



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")
port = raw_input("Enter port: ")







########The profile DB#########
con = Connection('localhost', int(port))
#con = Connection()
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']

#initiate a tags dict object
tags = collection.find_one({"horizon": {"$ne": None}})['horizon']

f = open('tags_'+str(c_id) +'.txt', 'w')
 
counter = 0
emptykeys = 0

for item in collection.find({"horizon": {"$ne": None}}):

	keys = item['horizon'].keys()
	
	if len(keys):
		counter += 1
		emptykeys +=1
		continue

	for key in keys:
		if key in tags:
			tags[key] += item['horizon']['key']
		else:
			tags.update({key: item['horizon']['key']})	
	
	counter += 1

f.write(json.dumps(tags))

print "counter: " + str(counter)
print "emptykeys: " + str(emptykeys)
	




