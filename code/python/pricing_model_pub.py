import sys
from numpy import *
from datetime import *
from pymongo import Connection

### disengagement criterion function 
def dis_fun(item):
    dis = 1
    if item.get('click_time')==None and item.get('open_time')==None:
        dis = -1
    try:
        #number_of_days = (datetime.now() - item.get('signup_time')).days
        number_of_days = (now - item.get('signup_time')).days
	if float(number_of_days)/7 <= 2:
            dis = 10
    except Exception:
        n=1
    try:
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if float(date_diff)/ET <= 1:
                dis = 0
    except Exception:
        n = 1

    return dis

###########Call to cmnd line to enter port, db name, collection name#####


client_id = raw_input("Enter client_id: ")

ET = raw_input("Set engagement threshold (default is 7 days): ")
if ET == '':
    ET = 7    

start = datetime.now()




####all the counters we'll need for Jan '11 - Jan '12 inclusive, (P stands for pageview of purchases dep. on type of client)
opens = [0]*13
clicks = [0]*13
P = [0]*13
emails = [0]*13
users = [0]*13
dormant = [0]*13

#user counts based on number of action >=1, >=2, ... >=10, 
O_users = [0]*10
C_users = [0]*10
P_users = [0]*10
for i in range(0,10):
    O_users[i] = [0]*13
    C_users[i] = [0]*13
    P_users[i] = [0]*13
    
#for the users who "act" at most 1, 2, ... 10 times
O_opens = [0]*10
O_clicks = [0]*10
O_P = [0]*10
C_opens = [0]*10
C_clicks = [0]*10
C_P = [0]*10
P_opens = [0]*10
P_clicks = [0]*10
P_P = [0]*10

for i in range(0,10):
    O_opens[i] = [0]*13
    O_clicks[i] = [0]*13
    O_P[i] = [0]*13
    C_opens[i] = [0]*13
    C_clicks[i] = [0]*13
    C_P[i] = [0]*13
    P_opens[i] = [0]*13
    P_clicks[i] = [0]*13
    P_P[i] = [0]*13




#########START the aggregation/cleaning#######
print 'Make sure limit it set correctly'


#########The profile DB#########
con = Connection('localhost', 40006)
db = con['sailthru']
collection = db['profile.'+str(client_id)]

for item in collection.find():
    
    signup_time = item.get('signup_time').date()
    su_month = signup_time.month
    if item.get('optout_time') == True:
        for m in range(su_month, 14):
            users[m] +=1
    else:
        o_month = item.get('optout_time').date().month
        for m in range(su_month, o_month+1):
            users[m] +=1
            
        

    message = item.get('daily_message')
    opens = item.get('daily_open')
    click = item.get('daily_click')
        
    #for 2011
    if signup_time.year == 2011:
        
        

        try:
            message_keys = item.get('daily_message').keys()
            opens_keys = item.get('daily_open').keys()
            for key in opens_keys:
                try:
                    datetime.strptime(key, '%y%m%d').date()
                    
                except Exception:
                    #print str(counter) + 'bad open key'
                    bad_open_key +=1
                else:
                    continue
        
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
            else:
                continue
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
            if (float(date_diff)/7 <= 1):
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
            if (float(date_diff)/7 <= 1):
                try:
                    ratio = float(click.get(key))/float(opens.get(key))
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
                      lists,
                      lists_remove,
                      lists_signup,
                      city,
                      state,
                      country,
                      geo_count,
                      optout,
                      #disengaged_prior,
                      disengaged]
    
    #change the None's to 0
    agg_list = none(agg_list)
    collection.update({'_id':  item.get('_id')}, {"$set": {'datascience.aggregate_list_eng' : agg_list}}, safe=True)

    counter +=1

end = datetime.now()
print (end-start).seconds
print str(bad_open_key) + 'bad open key'
print str(bad_click_key) + 'bad click key'
