import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")








########The profile DB#########
con = Connection('localhost', 40005)
#con = Connection('localhost', 40004)
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']




f = open(str(c_id)+'_trends.txt', 'w')


purch_count = [0]*400
open_count = [0]*400
click_count = [0]*400
pv_count = [0]*400
	
counter = 0
nodate = 0
nopurch = 0
noclick = 0
noopen = 0
nopv = 0
bad_cl_key = 0
bad_op_key = 0
bad_pv_key = 0





#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}]}):


for item in collection.find({"$and": [{"horizon_month": {"$ne": None}}, {"purchases": {"$ne": None}}, {"signup_time": {"$ne": None}}, {"daily_open": {"$ne": None}}, {"daily_click": {"$ne": None}}]}):


#       
#	signup_time = item.get('signup_time').date()
#	if signup_time.year == 2011:
#
#	    
#		purchases = item.get('purchases')
#
#       		for p in range(len(item.get('purchases'))):
#			try:
#               			d = -(signup_time - item.get('purchases')[p].get('time').date()).days
#               			purch_count[d] += 1
#			except:
#				nodate += 1
#	
#	
#		#CLICKS
#		
#		click_keys = item.get('daily_click').keys()
# 		for key in click_keys:
#			try:
#              			d = (datetime.strptime(key, '%y%m%d').date() - signup_time).days
#				click_count[d] += 1
#				
#                       	except Exception:
#               			bad_cl_key += 1
#	
#		#OPENS
#		open_keys = item.get('open_click').keys()
# 		for key in open_keys:
#			try:
#               			d = (datetime.strptime(key, '%y%m%d').date() - signup_time).days
#				open_count[d] += 1
#				
#                       	except Exception:
#               			bad_op_key += 1
#	
#
#		#PAGEVIEWS
#		  
#		
#		pageview_keys = item.get('horizon_month').keys()
#        	for key in pageview_keys:
#			try:
#              			d = (datetime.strptime(key, '%Y%m').date() - signup_time).days
#				pv_count[d] += 1 
#                        except Exception:
#        	      		bad_pv_key += 1
#	
#
#		counter +=1 
#
#f.close()
#print "counter = " + str(counter)
#print  "nodate = " + str(nodate)
#print "nopurch = " + str(nopurch)
#print "noclick = " + str(noclick)
#print "noopen = " + str(noopen)
#print "nopv = " + str(nopv)
#print "bad_cl_key = " + str(bad_cl_key) 
#print "bad_op_key = " + str(bad_op_key)
#print "bad_pv_key = " + str(bad_pv_key)
#
#

#for item in collection.find({"$and": [{"horizon_month": {"$exists": True}}, {"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}, {"daily_open": {"$exists": True}}, {"daily_click": {"$exists": True}}]}):

       
	signup_time = item.get('signup_time').date()
	if signup_time.year == 2011:

	        try:
			purchases = item.get('purchases')

        		for p in range(len(item.get('purchases'))):
				try:
                			d = -(signup_time - item.get('purchases')[p].get('time').date()).days
                			purch_count[d] += 1
				except:
					nodate += 1
		except:
			nopurch += 1

	
		#CLICKS
		try:
			click_keys = item.get('daily_click').keys()
 			for key in click_keys:
				try:
                    			d = (datetime.strptime(key, '%y%m%d').date() - signup_time).days
					click_count[d] += 1
				
                        	except Exception:
                    			bad_cl_key += 1
		except:
			noclick += 1

		#OPENS
		try:
			open_keys = item.get('open_click').keys()
 			for key in open_keys:
				try:
                    			d = (datetime.strptime(key, '%y%m%d').date() - signup_time).days
					open_count[d] += 1
					
                        	except Exception:
                    			bad_op_key += 1
		except:
			noopen += 1

		#PAGEVIEWS
		  
		try:
			pageview_keys = item.get('horizon_month').keys()
        		for key in pageview_keys:
				try:
                    			d = (datetime.strptime(key, '%Y%m').date() - signup_time).days
					pv_count[d] += 1 
                        	except Exception:
        	            		bad_pv_key += 1
		except:
			nopv += 1



		counter +=1 

f.close()
print "counter = " + str(counter)
print  "nodate = " + str(nodate)
print "nopurch = " + str(nopurch)
print "noclick = " + str(noclick)
print "noopen = " + str(noopen)
print "nopv = " + str(nopv)
print "bad_cl_key = " + str(bad_cl_key) 
print "bad_op_key = " + str(bad_op_key)
print "bad_pv_key = " + str(bad_pv_key)




