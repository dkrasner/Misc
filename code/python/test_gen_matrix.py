#########Generates a matrix from the aggregation list for every user########
import os
from datetime import *
import csv


###########Call to cmnd line to enter port, db name, collection name#####
port = raw_input("Enter port (if no port enter 0): ")
port = int(port)
if port==0:
    port = None
    
dbname = raw_input("Enter db name (dafault is 'sailthru'): ")
if dbname == '':
    dbname = 'sailthru'

profile = raw_input("Enter collection name: ")

filt = raw_input("Enter query filter (default is none): ")
if filt == '':
    filt = None
else:
    filt = eval(filt)

file_name = raw_input("Enter file name for the saved data: ")

    
#port = 40006
#profile = 'profile.450'

#connect to mongo
from pymongo import Connection
#con = Connection(mongo_host,  mongo_port)
con = Connection('localhost', port)
#db = con['sailthru']
db = con[dbname]
collection = db[profile]


#os.chdir('/data/dump')
start = datetime.now()


f = open(file_name, 'w')

for item in collection.find(filt):
    csv.writer(f).writerow(item.get('datascience').get('aggregate_list'))

    
f.close()

end = datetime.now()
print 'time ' + str((end-start).seconds)
