
from numpy import *
from datetime import *
from pymongo import Connection
import csv


###########Call to cmnd line to enter blast date####


date= raw_input("enter date: ")

    

start = datetime.now()

counter = 0

data = [0]*5000
for i in range(5000):
	data[i] = [i,0]


f = open('message.blast.'+str(date)+'.txt', 'w')


#########The profile DB#########
con = Connection('localhost', 40003)
db = con['sailthru']
collection = db['message.blast.'+str(date)]

for item in collection.find({'clicks': {'$ne': []}}):

	
	s_time = item.get('send_time')
	


	try:
		len_cl = len(item.get('clicks'))
		for c in range(len_cl):
			try:
					
				min_elapsed = ((item.get('clicks')[c].get('ts') - s_time).seconds)/60
				data[min_elapsed][1] += 1
			except Exception:
				continue 

	except Exception:
		nocl=1
 	
	counter += 1  

csv.writer(f).writerows(data)

f.close()
end = datetime.now()

print (end-start).seconds
print "counter: " + str(counter)

