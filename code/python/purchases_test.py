
from numpy import *
from datetime import *
from pymongo import Connection
import csv

#######get all indices from list based on value function
def all_indices(qlist, value):
    indices = []
    idx = -1
    while 1:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

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


c_id = raw_input("Enter client_id: ")

    

start = datetime.now()




####all the counters we'll need for Jan '11 - Jan '12 inclusive, (pv stands for pageview of purchases dep. on type of client)
opens = [0]*13
clicks = [0]*13
pv = [0]*13
emails = [0]*13
campaign_emails = [0]*13
users = [0]*13
subscribers_ave = [0]*13
subscribers_lastday = [0]*13
dormant = [0]*13
concierge = [0]*13
scout = [0]*13
ad_imp = [0]*13
ad_imp_click = [0]*13
nonreg_pv = [0]*13
all_pv = [0]*13
purchases_count = [0]*13
purchases_price = [0]*13


#user counts based on number of action <=1, <=2, ... <=10, 
O_users = [0]*10
C_users = [0]*10
pv_users = [0]*10
pur_cnt_users = [0]*10
for i in range(0,10):
    O_users[i] = [0]*13
    C_users[i] = [0]*13
    pv_users[i] = [0]*13
    pur_cnt_users[i] = [0]*13
    #pur_prc_users[i] = [0]*13

O_opens = [0]*10
O_clicks = [0]*10
O_pv = [0]*10
O_pur_cnt = [0]*10
O_pur_prc = [0]*10
C_opens = [0]*10
C_clicks = [0]*10
C_pv = [0]*10
C_pur_cnt = [0]*10
C_pur_prc = [0]*10
pv_opens = [0]*10
pv_clicks = [0]*10
pv_pv = [0]*10
pv_pur_cnt = [0]*10
pv_pur_prc = [0]*10
pur_cnt_opens = [0]*10
pur_cnt_clicks = [0]*10
pur_cnt_pv = [0]*10
pur_cnt_pur_cnt = [0]*10
pur_cnt_pur_prc = [0]*10
#pur_prc_opens = [0]*10
#pur_prc_clicks = [0]*10
#pur_prc_pv = [0]*10


for i in range(0,10):
    O_opens[i] = [0]*13
    O_clicks[i] = [0]*13
    O_pv[i] = [0]*13
    O_pur_cnt[i] = [0]*13
    O_pur_prc[i] = [0]*13
    C_opens[i] = [0]*13
    C_clicks[i] = [0]*13
    C_pv[i] = [0]*13
    C_pur_cnt[i] = [0]*13
    C_pur_prc[i] = [0]*13
    pv_opens[i] = [0]*13
    pv_clicks[i] = [0]*13
    pv_pv[i] = [0]*13
    pv_pur_cnt[i] = [0]*13
    pv_pur_prc[i] = [0]*13
    pur_cnt_opens[i] = [0]*13
    pur_cnt_clicks[i] = [0]*13
    pur_cnt_pv[i] = [0]*13
    pur_cnt_pur_cnt[i] = [0]*13
    pur_cnt_pur_prc[i] = [0]*13

    #pur_prc_opens[i] = [0]*13
    #pur_prc_clicks[i] = [0]*13
    #pur_prc_pv[i] = [0]*13

#user counts based on number of action >=1, >=2, ... >=10, 
Oge_users = [0]*10
Cge_users = [0]*10
pvge_users = [0]*10
pur_cntge_users = [0]*10
#pur_prcge_users = [0]*10

for i in range(0,10):
    Oge_users[i] = [0]*13
    Cge_users[i] = [0]*13
    pvge_users[i] = [0]*13
    pur_cntge_users[i] = [0]*13
   # pur_prcge_users[i] = [0]*13


Oge_opens = [0]*10
Oge_clicks = [0]*10
Oge_pv = [0]*10
Oge_pur_cnt = [0]*10
Oge_pur_prc = [0]*10
Cge_opens = [0]*10
Cge_clicks = [0]*10
Cge_pv = [0]*10
Cge_pur_cnt = [0]*10
Cge_pur_prc = [0]*10
pvge_opens = [0]*10
pvge_clicks = [0]*10
pvge_pv = [0]*10
pvge_pur_cnt = [0]*10
pvge_pur_prc = [0]*10
pur_cntge_opens = [0]*10
pur_cntge_clicks = [0]*10
pur_cntge_pv = [0]*10
pur_cntge_pur_cnt = [0]*10
pur_cntge_pur_prc = [0]*10


for i in range(0,10):
    Oge_opens[i] = [0]*13
    Oge_clicks[i] = [0]*13
    Oge_pv[i] = [0]*13
    Oge_pur_cnt[i] = [0]*13
    Oge_pur_prc[i] = [0]*13
    Cge_opens[i] = [0]*13
    Cge_clicks[i] = [0]*13
    Cge_pv[i] = [0]*13
    Cge_pur_cnt[i] = [0]*13
    Cge_pur_prc[i] = [0]*13
    pvge_opens[i] = [0]*13
    pvge_clicks[i] = [0]*13
    pvge_pv[i] = [0]*13
    pvge_pur_cnt[i] = [0]*13
    pvge_pur_prc[i] = [0]*13
    pur_cntge_opens[i] = [0]*13
    pur_cntge_clicks[i] = [0]*13
    pur_cntge_pv[i] = [0]*13
    pur_cntge_pur_cnt[i] = [0]*13
    pur_cntge_pur_prc[i] = [0]*13

#########START the aggregation/cleaning#######
print 'Make sure limit it set correctly'


#########The profile DB#########
con = Connection('localhost', 40006)
#con = Connection('localhost', 40004)
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']

#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"signup_time": {"$exists": True}}]}):
for item in db['profile.764'].find({"purchases": {"$exists": True}}).limit(3):
   
    temp_opens = [0]*13
    temp_clicks = [0]*13
    temp_pv = [0]*13
    temp_pur_cnt = [0]*13
    temp_pur_prc = [0]*13 


#############purchases############
    try:
	len_pur = len(item.get('purchases'))
	for p in range(len_pur):
		try:
			d = item.get('purchases')[i].get('time')
			if d.year == 2011:
				temp_pur_cnt[d.month] += 1
				temp_pur_prc[d.month] += float(item.get('purchases')[i].get('price'))/100
			if d.year == 2012:
				temp_pur_cnt[12+d.month] += 1
				temp_pur_prc[12+d.month] += float(item.get('purchases')[i].get('price'))/100
    		except Exception:
			nodate = 1
    except Exception:
	nopur = 1

    purchases_count = [purchases_count[i] + temp_pur_cnt[i] for i in range(0, len(purchases_count))]
    purchases_price = [purchases_price[i] + temp_pur_prc[i] for i in range(0, len(purchases_price))]


print "purchases_cnt" + str(purchases_count)
print "purchases_prc" + str(purchases_price)


######the users who ast atmost  once, twice,.... ten times#####
    for a in range(0, 10):
        for m in range(0,13):
                if temp_opens[m] <= a+1:
                        O_users[a][m] += 1
                        O_opens[a][m] += temp_opens[m]
                        O_clicks[a][m] += temp_clicks[m]
                        O_pv[a][m] += temp_pv[m]
                        O_pur_cnt[a][m] += temp_pur_cnt[m]
                        O_pur_prc[a][m] += temp_pur_prc[m]
                if temp_clicks[m] <= a+1:
                        C_users[a][m] += 1
                        C_opens[a][m] += temp_opens[m]
                        C_clicks[a][m] += temp_clicks[m]
                        C_pv[a][m] += temp_pv[m]
                        C_pur_cnt[a][m] += temp_pur_cnt[m]
                        C_pur_prc[a][m] += temp_pur_prc[m]
                if temp_pv[m] <= a+1:
                        pv_users[a][m] += 1
                        pv_opens[a][m] += temp_opens[m]
                        pv_clicks[a][m] += temp_clicks[m]
                        pv_pv[a][m] += temp_pv[m]
                        pv_pur_cnt[a][m] += temp_pur_cnt[m]
                        pv_pur_prc[a][m] += temp_pur_prc[m]
                if temp_pur_cnt[m] <= a+1:
                        pur_cnt_users[a][m] += 1
                        pur_cnt_opens[a][m] += temp_opens[m]
                        pur_cnt_clicks[a][m] += temp_clicks[m]
                        pur_cnt_pv[a][m] += temp_pv[m]
                        pur_cnt_pur_cnt[a][m] += temp_pur_cnt[m]
                        pur_cnt_pur_prc[a][m] += temp_pur_prc[m]


######the users who ast least  once, twice,.... ten times#####
    for a in range(0, 10):
        for m in range(0,13):
                if temp_opens[m] > a:
                        Oge_users[a][m] += 1
                        Oge_opens[a][m] += temp_opens[m]
                        Oge_clicks[a][m] += temp_clicks[m]
                        Oge_pv[a][m] += temp_pv[m]
                        Oge_pur_cnt[a][m] += temp_pur_cnt[m]
                        Oge_pur_prc[a][m] += temp_pur_prc[m]

                if temp_clicks[m] > a:
                        Cge_users[a][m] += 1
                        Cge_opens[a][m] += temp_opens[m]
                        Cge_clicks[a][m] += temp_clicks[m]
                        Cge_pv[a][m] += temp_pv[m]
                        Cge_pur_cnt[a][m] += temp_pur_cnt[m]
                        Cge_pur_prc[a][m] += temp_pur_prc[m]

                if temp_pv[m] > a:
                        pvge_users[a][m] += 1
                        pvge_opens[a][m] += temp_opens[m]
                        pvge_clicks[a][m] += temp_clicks[m]
                        pvge_pv[a][m] += temp_pv[m]
                        pvge_pur_cnt[a][m] += temp_pur_cnt[m]
                        pvge_pur_prc[a][m] += temp_pur_prc[m]

                if temp_pur_cnt[m] > a:
                        pur_cntge_users[a][m] += 1
                        pur_cntge_opens[a][m] += temp_opens[m]
                        pur_cntge_clicks[a][m] += temp_clicks[m]
                        pur_cntge_pv[a][m] += temp_pv[m]
                        pur_cntge_pur_cnt[a][m] += temp_pur_cnt[m]
                        pur_cntge_pur_prc[a][m] += temp_pur_prc[m]

print "pur_cnt_users: " str(pur_cnt_users)
print "pur_cnt_pur_cnt: " str(pur_cnt_pur_cnt)
print "pur_cnt_pur_prc: " str(pur_cnt_pur_prc)
print "pur_cntge_users: " str(pur_cntge_users)
print "pur_cntge_pur_cnt: " str(pur_cntge_pur_cnt)
print "pur_cntge_pur_prc: " str(pur_cntge_pur_prc)


