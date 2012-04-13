import sys
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
empty = [0]*10     # to replace purchase, pv bins if they aren't any pv's purchases ect
for i in range(0,10):
    O_users[i] = [0]*13
    C_users[i] = [0]*13
    pv_users[i] = [0]*13
    pur_cnt_users[i] = [0]*13
    empty[i] = [0]*13

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
for item in collection.find({"signup_time": {"$exists": True}}):
   
    	 
    signup_time = item.get('signup_time').date()
    su_month = signup_time.month
    
    temp_opens = [0]*13
    temp_clicks = [0]*13
    temp_pv = [0]*13
    temp_pur_cnt = [0]*13
    temp_pur_prc = [0]*13 
            
    #user and dormant counts

    if signup_time.year == 2012:
        try:
            o_month = item.get('optout_time').date().month
            #o_year = item.get('optout_time').date().year
            #if o_year == 2011:
            for m in range(12+su_month-1, 12+o_month-1):
		users[m] +=1
            if item.get('click_time')==none and item.get('open_time')==none:
                for m in range(12+su_month-1, 12+o_month-1):
			dormant[m] +=1
                
               # if o_year == 2012:
                #        for m in range(su_month-1, 12+o_month-1):
                 #               users[m] +=1
               # if item.get('click_time')==None and item.get('open_time')==None:
                #        for m in range(su_month-1, 12+o_month-1):
                 #               dormant[m] +=1

        except Exception:
            for m in range(12+su_month-1, 13):
                users[m] +=1
            if item.get('click_time')==None and item.get('open_time')==None:
                for m in range(12+su_month-1, 13):
                    dormant[m] +=1

    if signup_time.year == 2011:
       	try:
            o_month = item.get('optout_time').date().month
	    o_year = item.get('optout_time').date().year
	    if o_year == 2011:
            	for m in range(su_month-1, o_month-1):
                	users[m] +=1
            	if item.get('click_time')==None and item.get('open_time')==None:
                	for m in range(su_month-1, o_month-1):
				dormant[m] +=1
		
	    if o_year == 2012:
               	for m in range(su_month-1, 12+o_month-1):
                       	users[m] +=1
                if item.get('click_time')==None and item.get('open_time')==None:
                        for m in range(su_month-1, 12+o_month-1):
                        	dormant[m] +=1

        except Exception:
            for m in range(su_month-1, 13):
                users[m] +=1
            if item.get('click_time')==None and item.get('open_time')==None:
                for m in range(su_month-1, 13):
                    dormant[m] +=1

   
    if signup_time.year < 2011:
        try:
            o_month = item.get('optout_time').date().month
	    o_year = item.get('optout_time').date().year
	    if o_year == 2011:
	        for m in range(0, o_month-1):
        	     users[m] +=1
            	if item.get('click_time')==None and item.get('open_time')==None:
                     for m in range(0, o_month-1):
                         dormant[m] +=1
	    if o_year == 2012:
                for m in range(0, 12+o_month-1):
                     users[m] +=1
                if item.get('click_time')==None and item.get('open_time')==None:
                     for m in range(0, 12+o_month-1):
                         dormant[m] +=1
        except Exception:
            for m in range(0, 13):
                users[m] +=1
            if item.get('click_time')==None and item.get('open_time')==None:
                for m in range(0, 13):
                    dormant[m] +=1

    # open, click and pv counts
    try:
	opens_keys = item.get('daily_open').keys()
        #print opens_keys
	for key in opens_keys:
		try:
			d = datetime.strptime(key, '%y%m%d').date()
                    	o = item.get('daily_open').get(key)
                    	if d.year == 2011:
                        	temp_opens[d.month-1] += o
                        
                    	if d.year == 2012:
                        	temp_opens[12+d.month-1] += o
                except Exception:
                    	bad_open_key =1
                
    except Exception:	
	nothing = 1

    try:
	click_keys = item.get('daily_click').keys()
        #print click_keys
	for key in click_keys:
		try:
			d = datetime.strptime(key, '%y%m%d').date()
                    	c = item.get('daily_click').get(key)
                    	if d.year == 2011:
                        	temp_clicks[d.month-1] += c
                        
                    	if d.year == 2012:
                        	temp_clicks[12+d.month-1] += c
                except Exception:
			bad_click_key =1
                
    except Exception:
	nothing = 1

    try:
	pageview_keys = item.get('horizon_month').keys()
       # print pageview_keys
        for key in pageview_keys:
		try:
                    	d = datetime.strptime(key, '%Y%m').date()
                    	p = item.get('horizon_month').get(key).get('_count')
                    	if d.year == 2011:
                        	temp_pv[d.month-1] += p
                        
                    	if d.year == 2012:
                        	temp_pv[12+d.month-1] += p
                except Exception:
                    	bad_pv_key =1
                
    except Exception:
	nothing = 1

    opens = [opens[i] + temp_opens[i] for i in range(0, len(opens))]
    clicks = [clicks[i] +  temp_clicks[i] for i in range(0, len(clicks))]
    pv = [pv[i] + temp_pv[i] for i in range(0, len(pv))]
       

#############purchases############
    try:
	len_pur = len(item.get('purchases'))
	for p in range(0,len_pur):
		try:
			d = item.get('purchases')[p].get('time')
			if d.year == 2011:
				temp_pur_cnt[d.month] += 1
				temp_pur_prc[d.month] += float(item.get('purchases')[p].get('price'))/100
			if d.year == 2012:
				temp_pur_cnt[12+d.month] += 1
				temp_pur_prc[12+d.month] += float(item.get('purchases')[p].get('price'))/100
    		except Exception:
			nodate = 1
    except Exception:
	nopur = 1

    purchases_count = [purchases_count[i] + temp_pur_cnt[i] for i in range(0, len(purchases_count))]
    purchases_price = [purchases_price[i] + temp_pur_prc[i] for i in range(0, len(purchases_price))]


	##############The Bins########

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


    ####### make sure that bins without pv's or purchases don't get users counted 
    if pv == [0]*13:
	pv_users = empty
	pv_opens = empty
	pv_clicks = empty
	pv_pv = empty
	pv_pur_cnt = empty
	pv_pur_prc = empty
    if purchases_count == [0]*13:
	pur_cnt_users = empty
	pur_cnt_opens = empty
	pur_cnt_clicks = empty
	pur_cnt_pv = empty
	pur_cnt_pur_cnt = empty
	pur_cnt_pur_prc = empty
	
    #print "temp_opens: " + str(temp_opens)
    #print "temp_clicks: " + str(temp_clicks)
    #print "temp_pv: " + str(temp_pv)
	
#########The horizon DB#########
con = Connection('localhost', 40002)
db = con['sailthru']

#concierge
collection = db['stats.recommend.day']

for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"day": {"$exists": True}}]}):
    d = datetime.strptime(str(item.get("day")), '%Y%m%d').date()
    
    if d.year == 2011:
        try:
		concierge[d.month-1] += item.get("recommend_hit")
	except Exception:
		nohit = 1
    if d.year ==2012:
	try:
        	concierge[12+d.month-1] += item.get("recommend_hit")
        except Exception:
		nohit = 1

############pvage views###########
collection = db['stats.pv.day']

for item in collection.find({"_id" : {'$regex': '^'+str(c_id)+'_.*'}}):
    d = datetime.strptime(str(item.get("day")), '%Y%m%d').date()

    if d.year == 2011:
        try:
                all_pv[d.month-1] += item.get("pv")
        except Exception:
                nopv = 1
    if d.year ==2012:
        try:
                all_pv[12+d.month-1] += item.get("pv")
        except Exception:
                nopv = 1


nonreg_pv = [all_pv[i] - pv[i] for i in range(0, len(nonreg_pv))]

###########The Main DB############
con = Connection('localhost', 40001)
db = con['sailthru']

#unique list subscribers
collection =  db['stats.list.day']

temp_subs = [0]*13
for i in range(0,13):
	temp_subs[i] = [0]*31


for item in collection.find({"$and": [{"client_id":  int(c_id)}, {'list': ""}, {"day": {"$exists": True}}]}):
    d = datetime.strptime(str(item.get("day")), '%Y%m%d').date()
    
    if d.year == 2011:
        try:
                temp_subs[d.month-1][d.day-1] += item.get("email_count")
        except Exception:
                nolist = 1
    if d.year == 2012:
        try:
                temp_subs[12+d.month-1][d.day-1] += item.get("email_count")
        except Exception:
                nolist = 1

for m in range(0, 13):
	try:
		indices = all_indices(temp_subs[m], 0)
		days = len(indices)
		last_day = max(list(set(range(0,31)) - set(indices)))
		subscribers_ave[m] = float(sum(temp_subs[m]))/float(31-days)  
		subscribers_lastday[m] = temp_subs[m][last_day]
	except Exception:
		subscribers_ave[m] = average(temp_subs[m])
		subscribers_lastday[m] = temp_subs[m][30]


#scout
collection = db['stats.scout.day']

for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"day": {"$exists": True}}]}):
    d = datetime.strptime(str(item.get("day")), '%Y%m%d').date()
    
    if d.year == 2011:
        try:
                scout[d.month-1] += item.get("hit")
        except Exception:
                nohit = 1
    if d.year ==2012:
        try:
                scout[12+d.month-1] += item.get("hit")
        except Exception:
                nohit = 1

#emails        
collection = db['stats.client.day']
for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"day": {"$exists": True}}, {"blast": {"$exists": True}}]}):
    d = datetime.strptime(str(item.get("day")), '%Y%m%d').date()

    if d.year == 2011:
	campaign_emails[d.month-1] += item.get("blast").get("total")
        try:
                emails[d.month-1] += item.get("blast").get("total") + item.get("send").get("total")
        except Exception:
                emails[d.month-1] += item.get("blast").get("total") 
    if d.year ==2012:
	campaign_emails[12+d.month-1] += item.get("blast").get("total")
        try:
                emails[12+d.month-1] += item.get("blast").get("total") + item.get("send").get("total")
        except Exception:
                emails[12+d.month-1] += item.get("blast").get("total")


#ad impressions
collection_b = db['stats.blast']
collection_s = db['stats.send']
temp_imp_b = [0]*13
temp_cl_b = [0]*13
temp_imp_s = [0]*13
temp_cl_s = [0]*13

for item in collection_s.find({"$and": [{"client_id":  int(c_id)}, {"banners": {"$exists": True}}, {"banners": {"$ne": []}}]}):
	
	
   d = datetime.strptime(str(item.get("day")), '%Y%m%d').date()
   if d.year == 2011:
	try:
		for i in range(0, len(item.get("banners"))):
			try:
				temp_imp_s[d.month-1] += item.get("banners")[i].get("imp")
			except Exception:
				noimp = 1
			try:
				temp_cl_s[d.month-1] += item.get("banners")[i].get("click_total")
			except Exception:
				nocl = 1
  	except Exception:
		noban = 1
                  
   if d.year == 2012:		
        try:
                for i in range(0, len(item.get("banners"))):
                        try:
                                temp_imp_s[12+d.month-1] += item.get("banners")[i].get("imp")
                        except Exception:
                                noimp = 1
                        try:
                                temp_cl_s[12+d.month-1] += item.get("banners")[i].get("click_total")
                        except Exception:
                                nocl = 1
	except Exception:
		noban=1
       
		


ad_imp = [temp_imp_b[i] + temp_imp_s[i] for i in range(0, len(ad_imp))]
ad_imp_click = [temp_cl_b[i] + temp_cl_s[i] for i in range(0, len(ad_imp_click))]

			








f = open(str(c_id)+'_pricing_model.txt', 'w')
g = open(str(c_id)+'_pricing_model_extras.txt', 'w')

csv.writer(f).writerow(users)
csv.writer(f).writerow(subscribers_ave)
csv.writer(f).writerow(subscribers_lastday)
csv.writer(f).writerow(dormant)
csv.writer(f).writerow(opens)
csv.writer(f).writerow(clicks)
csv.writer(f).writerow(pv)
csv.writer(f).writerow(purchases_count)
csv.writer(f).writerow(purchases_price)
csv.writer(f).writerow(concierge)
csv.writer(f).writerow(scout)
csv.writer(f).writerow(emails)
csv.writer(f).writerow(campaign_emails)
csv.writer(f).writerow(ad_imp)
csv.writer(f).writerow(ad_imp_click)
csv.writer(f).writerow(all_pv)
csv.writer(f).writerow(nonreg_pv)


csv.writer(g).writerows(O_users)
csv.writer(g).writerows(O_opens)
csv.writer(g).writerows(O_clicks)
csv.writer(g).writerows(O_pv)
csv.writer(g).writerows(O_pur_cnt)
csv.writer(g).writerows(O_pur_prc) 
csv.writer(g).writerows(C_users) 
csv.writer(g).writerows(C_opens) 
csv.writer(g).writerows(C_clicks) 
csv.writer(g).writerows(C_pv) 
csv.writer(g).writerows(C_pur_cnt)
csv.writer(g).writerows(C_pur_prc) 
csv.writer(g).writerows(pv_users) 
csv.writer(g).writerows(pv_opens) 
csv.writer(g).writerows(pv_clicks) 
csv.writer(g).writerows(pv_pv) 
csv.writer(g).writerows(pv_pur_cnt)
csv.writer(g).writerows(pv_pur_prc) 
csv.writer(g).writerows(pur_cnt_users) 
csv.writer(g).writerows(pur_cnt_opens) 
csv.writer(g).writerows(pur_cnt_clicks) 
csv.writer(g).writerows(pur_cnt_pv) 
csv.writer(g).writerows(pur_cnt_pur_cnt)
csv.writer(g).writerows(pur_cnt_pur_prc) 

csv.writer(g).writerows(Oge_users) 
csv.writer(g).writerows(Oge_opens) 
csv.writer(g).writerows(Oge_clicks) 
csv.writer(g).writerows(Oge_pv) 
csv.writer(g).writerows(Oge_pur_cnt)
csv.writer(g).writerows(Oge_pur_prc) 
csv.writer(g).writerows(Cge_users) 
csv.writer(g).writerows(Cge_opens)
csv.writer(g).writerows(Cge_clicks)
csv.writer(g).writerows(Cge_pv)
csv.writer(g).writerows(Cge_pur_cnt)
csv.writer(g).writerows(Cge_pur_prc)  
csv.writer(g).writerows(pvge_users) 
csv.writer(g).writerows(pvge_opens) 
csv.writer(g).writerows(pvge_clicks) 
csv.writer(g).writerows(pvge_pv)
csv.writer(g).writerows(pvge_pur_cnt)
csv.writer(g).writerows(pvge_pur_prc)  
csv.writer(g).writerows(pur_cntge_users) 
csv.writer(g).writerows(pur_cntge_opens) 
csv.writer(g).writerows(pur_cntge_clicks) 
csv.writer(g).writerows(pur_cntge_pv) 
csv.writer(g).writerows(pur_cntge_pur_cnt)
csv.writer(g).writerows(pur_cntge_pur_prc) 





f.close()
g.close()


   
end = datetime.now()
print "users: " + str(users)
print "subscribers_ave: " + str(subscribers_ave)
print "subscribers_lastday: " + str(subscribers_lastday)
print "dormant: " + str(dormant)
print "opens: " + str(opens)
print "clicks: " + str(clicks)
print "pv: " + str(pv)
print "purchases_count: " + str(purchases_count)
print "purchases_price: " + str(purchases_price)
print "concierge: " + str(concierge)
print "scout: " + str(scout)
print "emails: " + str(emails)
print "camp. emails: " + str(campaign_emails)
print "ad_imp: " + str(ad_imp)
print "ad_imp_click: " + str(ad_imp_click)
print "all_pv: " + str(all_pv)
print "nonreg_pv: " + str(nonreg_pv)


#print "O_users: " +  str(O_users)
#print "C_users: " +  str(C_users)
#print "pv_users: " +  str(pv_users)
#print "O_opens: " +  str(O_opens)
#print "O_clicks: " +  str(O_clicks)
#print "O_pv: " +  str(O_pv)
#print "C_opens: " +  str(C_opens)
#print "C_clicks: " +  str(C_clicks)
#print "C_pv: " +  str(C_pv)
#print "pv_opens: " +  str(pv_opens)
#print "pv_clicks: " +  str(pv_clicks)
#print "pv_pv: " +  str(pv_pv)
#print "Oge_users: " +  str(Oge_users)
#print "Cge_users: " +  str(Cge_users)
#print "pvge_users: " +  str(pvge_users)
#print "Oge_opens: " +  str(Oge_opens)
#print "Oge_clicks: " +  str(Oge_clicks)
#print "Oge_pv: " +  str(Oge_pv)
#print "Cge_opens: " +  str(Cge_opens)
#print "Cge_clicks: " +  str(Cge_clicks)
#print "Cge_pv: " +  str(Cge_pv)
#print "pvge_opens: " +  str(pvge_opens)
#print "pvge_clicks: " +  str(pvge_clicks)
#print "pvge_pv: " +  str(pvge_pv)



print (start-end).seconds
