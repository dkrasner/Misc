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



# #SET engagement threshold in days
# ET = 7


start = datetime.now()

# #connect to mongo
# from pymongo import Connection
# #con = Connection(mongo_host,  mongo_port)
# con = Connection()
# db = con['sailthru']
# profile = 'profile.764'   #SET profile
# collection = db[profile]

# #figure when the collection was last updated - IMPORTANT: change this below if collection is current
# now = datetime.strptime('050101', '%y%m%d')
# for item in collection.find():
#     t = item.get('ts')
#     try:
#         if t > now:
#             now = t
#     except Exception:
#         temp = 1

counter = 0
no_opens_cnt = 0

print 'Make sure limit it set correctly'
for item in collection.find():
    
    disengaged = 1   #default is disengaged

    #if users is in the system for <= 2 weeks then he is considered engaged
    try:
        #number_of_days = (datetime.now() - item.get('signup_time')).days
        number_of_days = (now - item.get('signup_time')).days
	if number_of_days/7 <= 2:
            disengaged = 0
            collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.disengaged' : disengaged}}, safe=True)
            counter ++ 1
            continue
    except Exception:
        number_of_days = None

    

    try:
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if date_diff/ET <= 1:
                disengaged = 0
    except Exception:
	disengaged = -1 #if user has never engaged 
        no_opens_cnt +=1 

    collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.disengaged' : disengaged}}, safe=True)

    counter +=1

end = datetime.now()
print 'time: ' + str((end-start).seconds)
print str(no_opens_cnt) + ' no opens'

