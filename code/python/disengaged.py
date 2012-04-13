# import sys
# from numpy import *
# from datetime import *

# # if len(sys.argv) != 2:
# #     sys.exit("Mongo host information required: <host_name>:<port_no>")

# # host_info = sys.argv[1];

# # host_info_splits = host_info.split(":")
# # if len(host_info_splits) != 2:
# #     sys.exit("Invalid host information: " + host_info)

# # mongo_host = host_info_splits[0]
# # mongo_port = int(host_info_splits[1])







###########Call to cmnd line to enter port, db name, collection name#####
port = raw_input("Enter port (if no port enter 0): ")
port = int(port)
if port==0:
    port = None
    
dbname = raw_input("Enter db name (default is 'sailthru'): ")
if dbname == '':
    dbname = 'sailthru'

profile = raw_input("Enter collection name: ")

ET = raw_input("Set engagement threshold (default is 7 days): ")
if ET == '':
    ET = 7

    
filt = raw_input("Enter query filter (default is none): ")
if filt == '':
    filt = None
else:
    filt = eval(filt)

start = datetime.now()



#port = 40006
#profile = 'profile.450'

#connect to mongo
from pymongo import Connection
#con = Connection(mongo_host,  mongo_port)
con = Connection('localhost', port)
#db = con['sailthru']
db = con[dbname]
collection = db[profile]
#figure when the collection was last updated - IMPORTANT: change this below if collection is current
now = datetime.strptime('050101', '%y%m%d')
for item in collection.find():
    t = item.get('ts')
    try:
        if t > now:
            now = t
    except Exception:
        temp = 1

counter = 0
no_opens_cnt = 0


#start = datetime.now()

# print 'Make sure limit it set correctly'
# for item in collection.find(filt):
    
#     disengaged = 1   #default is disengaged

#     #if users is in the system for <= 2 weeks then he is considered engaged
#     try:
#         #number_of_days = (datetime.now() - item.get('signup_time')).days
#         number_of_days = (now - item.get('signup_time')).days
# 	if float(number_of_days)/7 <= 2:
#             disengaged = 10
#             collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.disengaged' : disengaged}}, safe=True)
#             counter += 1
#             continue
#     except Exception:
#         number_of_days = None

#     ###this is the 'dormant' condition
#     if item.get('click_time')==None and item.get('open_time')==None:
#         disengaged = -1
#         collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.disengaged' : disengaged}}, safe=True)
#         counter += 1
#         continue

#     try:
#         opens_keys = item.get('daily_open').keys()
#         for key in opens_keys:
#             date_diff = (now - datetime.strptime(key, '%y%m%d')).days
#             if float(date_diff)/ET <= 1:
#                 disengaged = 0
#     except Exception:
#         no_opens_cnt +=1
    
#     collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.disengaged' : disengaged}}, safe=True)

#     counter +=1

# end = datetime.now()
# print 'time: ' + str((end-start).seconds)
# print str(no_opens_cnt) + ' no opens'

