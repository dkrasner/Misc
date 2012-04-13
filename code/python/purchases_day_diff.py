import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv



###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")








#########The profile DB#########
#con = Connection('localhost', 40005)
con = Connection('localhost', 40004)
db = con['sailthru']
#collection = db['profile.'+str(c_id)]
collection = db['profile']


f = open(str(c_id)+'_purchase_data.txt', 'w')

start = datetime.now()


purch_counts = [0]*12
for i in range(12):
        purch_counts[i] = [0]*5


counter = 0
nodate = 0
#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}]}):
for item in collection.find({"purchases": {"$exists": True}}):


        creation_date = item.get('_id').generation_time.date()

        if creation_date.year == 2011:

                purchases = item.get('purchases')

                l = len(item.get('purchases')):
                if l > 0:       
                        if l==1:
				try:
					if item.get('purchases')[0].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[0].get('time').date().month
						purch_counts[m][0] += 1
				except Exception:
					nodate +=1

                        if l==2:
				try:
					if item.get('purchases')[0].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[0].get('time').date().month
						purch_counts[m][0] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[1].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[1].get('time').date().month
						purch_counts[m][1] += 1
				except Exception:
					nodate +=1

                        if l > 2 and l < 6:
				try:
					if item.get('purchases')[0].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[0].get('time').date().month
						purch_counts[m][0] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[1].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[1].get('time').date().month
						purch_counts[m][1] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[2].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[2].get('time').date().month
						purch_counts[m][2] += 1
				except Exception:
					nodate +=1

                        if l > 5 and l < 11:
				try:
					if item.get('purchases')[0].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[0].get('time').date().month
						purch_counts[m][0] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[1].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[1].get('time').date().month
						purch_counts[m][1] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[2].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[2].get('time').date().month
						purch_counts[m][2] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[5].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[5].get('time').date().month
						purch_counts[m][5] += 1
				except Exception:
					nodate +=1
                        
			if l > 10:
                                               
				try:
					if item.get('purchases')[0].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[0].get('time').date().month
						purch_counts[m][0] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[1].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[1].get('time').date().month
						purch_counts[m][1] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[2].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[2].get('time').date().month
						purch_counts[m][2] += 1
				except Exception:
					nodate +=1
				try:
					if item.get('purchases')[5].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[5].get('time').date().month
						purch_counts[m][5] += 1
				except Exception:
					nodate +=1

				try:
					if item.get('purchases')[10].get('time').date().year == 2011:
						m = creation_date.month - item.get('purchases')[10].get('time').date().month
						purch_counts[m][10] += 1
				except Exception:
					nodate +=1

                        
        counter +=1

csv.writer(f).writerows(purch_counts)


f.close()
print counter
print nodate
print (start - datetime.now()).seconds

#f = open(str(c_id)+'_purchase_date_diff.txt', 'w')
#
#start = datetime.now()
#
#
#counter = 0
#nodate = 0
#for item in collection.find({"$and": [{"client_id":  int(c_id)}, {"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}]}):
##for item in collection.find({"$and": [{"purchases": {"$exists": True}}, {"signup_time": {"$exists": True}}]}):
#
#       
#	signup_time = item.get('signup_time').date()
#
#        purchases = item.get('purchases')
#
#        for p in range(len(item.get('purchases'))):
#		try:
#                	days = -(signup_time - item.get('purchases')[p].get('time').date()).days
#                	csv.writer(f).writerow([counter, days])
#		except Exception:
#			nodate += 1
#	counter +=1 
#
#f.close()
#print counter
#print nodate
#      

