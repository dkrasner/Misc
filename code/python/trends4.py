import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")
port = raw_input("Enter port: ")







########The profile DB#########
con = Connection('localhost', int(port))
#con = Connection()
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']




#f_purch = open(str(c_id)+'_purch_trends.txt', 'w')
f = open(str(c_id)+'_behav_rates.txt', 'w')


counter = 0
bad_hor = 0
nopurch = 0

nohor = 0
noclick = 0
noopen = 0

bad_cl_key = 0
bad_op_key = 0
bad_pur_key = 0




for item in collection.find({"signup_time": {"$ne": None}}):

	
    signup_time = item.get('signup_time').date()

    keys = item.keys()
#   print keys

    ##################

    if 'horizon' in keys:
    	hor = 1	
    else:
    	hor = 0
    	nohor += 1	

   ##################
    
	
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
            else:
                continue
	open_per_message_avg = average(open_per_message)
    except Exception:
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
            else:
                continue
        click_per_open_avg = average(click_per_open)
    except Exception:
        click_per_open_avg = 0



    v = [hor, open_per_message_avg, click_per_open_avg] 
    if v == [0, 0, 0] or v == [1, 0, 0]:
    	counter += 1
    else:
    	csv.writer(f).writerow([hor, open_per_message_avg, click_per_open_avg])
    	counter +=1 




f.close()



print "counter = " + str(counter)
print "bad_hor = " + str(bad_hor)

print "nopurch = " + str(nopurch)
print "nohor = " + str(nohor)
print "noclick = " + str(noclick)
print "noopen = " + str(noopen)


print "bad_cl_key = " + str(bad_cl_key) 
print "bad_op_key = " + str(bad_op_key)
print "bad_pur_key = " + str(bad_pur_key)

