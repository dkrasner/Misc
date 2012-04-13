import sys
from numpy import *
from datetime import *
import csv
    

###########Call to cmnd line to enter port, db name, collection name#####
port = raw_input("Enter port (if no port enter 0): ")
port = int(port)
if port==0:
    port = None
    
dbname = raw_input("Enter db name (default is 'sailthru'): ")
if dbname == '':
    dbname = 'sailthru'

profile = raw_input("Enter collection name: ")

filt = raw_input("Enter query filter (default is none): ")
if filt == '':
    filt = None
else:
    filt = eval(filt)

ET = raw_input("Set engagement threshold (default is 7 days): ")
if ET == '':
    ET = 7    

start = datetime.now()


#connect to mongo

from pymongo import Connection
#con = Connection(mongo_host,  mongo_port)
con = Connection('localhost', port)
#db = con['sailthru']
db = con[dbname]
collection = db[profile]


counter = 0
### file to write non-dormants to
#f = open(profile+'_eng_'+str(2)+'_'+str(datetime.now().date())+'.txt', 'w')
f = open(profile+'_eng_pred_'+str(datetime.now().date())+'.txt', 'w')

#########START the aggregation/cleaning#######
print 'Make sure limit it set correctly'
for item in collection.find({'datascience.disengagement_prediction': {'$exists': True}}):
    ID = item.get('_id')
    dis_pred = item.get('datascience').get('disengagement_prediction')    
   
    csv.writer(f).writerow([ID, dis_pred])

f.close()

end = datetime.now()
print (end-start).seconds
print 'counter' + str(counter)
