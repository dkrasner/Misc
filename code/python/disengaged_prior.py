import sys
from numpy import *
from datetime import *

execfile('dis_fun_prior.py')
execfile('dis_fun.py')


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
    ET=7

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



# #figure when the collection was last updated - IMPORTANT: change this below if collection is current
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


start = datetime.now()

print 'Make sure limit it set correctly'
for item in collection.find(filt):
    
    disengaged = 1   #default is disengaged
    rec_open_per_message = 0
    rec_click_per_open = 0
    
    #if user is in the system for <= 2 weeks then he is considered "new"
    try:
        #number_of_days = (datetime.now() - item.get('signup_time')).days
        number_of_days = (now - item.get('signup_time')).days
	if float(number_of_days)/7 <= 2:
            disengaged = 10
            rec_open_per_message_avg = 10
            rec_click_per_open_avg = 10
            counter += 1
            dis_vec = []
            #dis_vec = [counter, disengaged]
            dis_vec.append(rec_open_per_message_avg)
            dis_vec.append(rec_click_per_open_avg)
            dis_vec.append(disengaged)
            collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.week_before_eng' : dis_vec}}, safe=True)
            #print dis_vec
            continue
    except Exception:
        number_of_days = None

    

    try:
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if (float(date_diff)/ET >= 1) and (float(date_diff)/ET <= 2):
                disengaged = 0
    except Exception:
        no_opens_cnt +=1

    

    ### deal with recent behavioral
    message = item.get('daily_message')
    opens = item.get('daily_open')
    click = item.get('daily_click')
    
    rec_open_per_message = []
    rec_click_per_open = []

    try:
        message_keys = item.get('daily_message').keys()
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
           #date_diff = (datetime.now() - datetime.strptime(k[0], '%y%m%d')).days
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if (float(date_diff)/ET >= 1) and (float(date_diff)/ET <= 2):
                try:
                    ratio = float(opens.get(key))/float(message.get(key))
                    rec_open_per_message.append(ratio)
                except Exception:
                    #print str(counter) + 'bad open key'
                    rec_open_per_message.append(0)
        if len(rec_open_per_message) > 0:
            rec_open_per_message_avg = average(rec_open_per_message)
            disengaged = 0
        else:
            rec_open_per_message_avg = 0
    except Exception:
        rec_open_per_message_avg = 0 

    try:
        click_keys = item.get('daily_click').keys()
        opens_keys = item.get('daily_open').keys()
        for key in click_keys:
            #date_diff = (datetime.now() - datetime.strptime(k[0], '%y%m%d')).days
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if (float(date_diff)/ET >= 1) and (float(date_diff)/ET <= 2):
                try:
                    ratio = float(click.get(key))/float(opens.get(key))
                    rec_click_per_open.append(ratio)
                except Exception:
                    #print str(counter) + 'bad open key'
                    rec_click_per_open.append(0)
        if len(rec_click_per_open) > 0:
            rec_click_per_open_avg = average(rec_click_per_open)
        else:
            rec_click_per_message_avg = 0
    except Exception:
        rec_click_per_open_avg = 0

    ###this is the 'dormant' condition
    if item.get('click_time')==None and item.get('open_time')==None:
        disengaged = -1



    dis_vec = [rec_open_per_message_avg,
                 rec_click_per_open_avg,
                 disengaged]
                 
    #dis_vec = [counter, disengaged]
    #dis_vec.append(rec_open_per_message_avg)
    #dis_vec.append(rec_click_per_open_avg)
    #dis_vec.append(disengaged)
    collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.week_before_eng' : dis_vec}}, safe=True)
    #print dis_vec
    counter +=1

end = datetime.now()
print 'time: ' + str((end-start).seconds)
print str(no_opens_cnt) + ' no opens'

