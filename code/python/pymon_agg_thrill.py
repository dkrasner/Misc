import sys
from numpy import *
from datetime import *

# if len(sys.argv) != 2:
#     sys.exit("Mongo host information required: <host_name>:<port_no>")

# host_info = sys.argv[1];

# host_info_splits = host_info.split(":")
# if len(host_info_splits) != 2:
#     sys.exit("Invalid host information: " + host_info)

# mongo_host = host_info_splits[0]
# mongo_port = int(host_info_splits[1])

# set all None's to 0
def none(l):
    for i in range(0, len(l)):
        if l[i] == None:
            l[i] = 0;
    return l;
    
###########Call to cmnd line to enter port, db name, collection name#####
port = raw_input("Enter port (if no port enter 0): ")
port = int(port)
if port==0:
    port = None
    
dbname = raw_input("Enter db name: ")

profile = raw_input("Enter collection name: ")


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
bad_click_key = 0
bad_open_key = 0

print 'Make sure limit it set correctly'
for item in collection.find({"$and": [{"lists": {"$exists":True}}, {"lists": {"$ne": []}}]}):
    #ID = item.get('_id')
    click_count = item.get('click_count')
    lifetime_click = item.get('lifetime_click')
    lifetime_message = item.get('lifetime_message')
    lifetime_open = item.get('lifetime_open')
    open_count = item.get('open_count')
    order = item.get('order')
    disengaged = item.get('datascience').get('disengaged')
    try:
        #number_of_days = (datetime.now() - item.get('signup_time')).days
        number_of_days = (now - item.get('signup_time')).days
    except Exception:
        number_of_days = None
    #Important: optout is 0 only if no optout has occured, i.e. not list specific
    if item.get('optout') == None:
        optout = 0;
    else:
        optout = 1;
    

    #deal with behavioral
    message = item.get('daily_message')
    opens = item.get('daily_open')
    click = item.get('daily_click')
    
   
    open_per_message = []
    click_per_open = []
    
 

    try:
        message_keys = item.get('daily_message').keys()
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
            try:
                ratio = float(opens.get(key))/float(message.get(key))
                open_per_message.append(ratio)
            except Exception:
                #print str(counter) + 'bad open key'
                bad_open_key +=1
        open_per_message_max  = max(open_per_message)
        open_per_message_min = min(open_per_message)
        open_per_message_avg = average(open_per_message)
    except Exception:
        open_per_message_max = 0
        open_per_message_min = 0
        open_per_message_avg = 0 

    try:
        click_keys = item.get('daily_click').keys()
        opens_keys = item.get('daily_open').keys()
        for key in click_keys:
            try:
                ratio = float(click.get(key))/float(opens.get(key))
                click_per_open.append(ratio)
            except Exception:
                #print str(counter) + 'bad click key'
                bad_click_key +=1
        click_per_open_max = max(click_per_open)
        click_per_open_min = min(click_per_open)
        click_per_open_avg = average(click_per_open)
    except Exception:
        click_per_open_max = 0
        click_per_open_min = 0

        click_per_open_avg = 0

    # deal with recent behavioral
    rec_open_per_message = []
    rec_click_per_open = []

    try:
        message_keys = item.get('daily_message').keys()
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
           #date_diff = (datetime.now() - datetime.strptime(k[0], '%y%m%d')).days
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if float(date_diff)/7 <= 1:
                try:
                    ratio = float(opens.get(key))/float(message.get(key))
                    rec_open_per_message.append(ratio)
                except Exception:
                    #print str(counter) + 'bad open key'
                    rec_open_per_message.append(0)
        if len(rec_open_per_message) > 0:
            rec_open_per_message_avg = average(rec_open_per_message)
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
            if float(date_diff)/7 <= 1:
                try:
                    ratio = float(opens.get(key))/float(message.get(key))
                    rec_click_per_open.append(ratio)
                except Exception:
                    #print str(counter) + 'bad open key'
                    rec_click_per_open.append(0)
        if len(rec_click_per_open) > 0:
            rec_click_per_open_avg = average(rec_click_per_open)
        else:
            rec_open_per_message_avg = 0
    except Exception:
        rec_click_per_open_avg = 0

        
    #append aggregation list into mongo
    agg_list = [click_count, 
                      lifetime_click,
                      lifetime_message,
                      lifetime_open,
                      open_count,
                      order,
                      number_of_days,
                      open_per_message_max,
                      open_per_message_min,
                      open_per_message_avg,
                      rec_open_per_message_avg,
                      click_per_open_max,
                      click_per_open_min,
                      click_per_open_avg,
                      rec_click_per_open_avg,
                      optout,
                      disengaged]
    #change the None's to 0
    agg_list = none(agg_list)
    collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.aggregate_list' : agg_list}}, safe=True)

    counter +=1

end = datetime.now()
print (end-start).seconds
print str(bad_open_key) + 'bad open key'
print str(bad_click_key) + 'bad click key'
