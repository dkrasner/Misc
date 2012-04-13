import sys
from unidecode import unidecode
import ast
import time
import simplejson as json
import csv
import urllib2 as urllib
from datetime import *


f = open('data/loggarics/snapshots/scribe-logs_horizonlog_2012-03-14_450.log', 'r')
g = open('data/loggarics/snapshots/timegeo_horizonlog_2012-03-14_450.txt', 'w')	

counter = 0 

def ip_geo(IP):
	
	query='http://api.ipinfodb.com/v3/ip-city/?key=89a3128e860665fa7037930ef2ea8ddc1b805f7c2378b9a59a46bf8361f94835&ip=' + str(IP) + '&format=json'	
	result = ast.literal_eval(urllib.urlopen(query).read())
	
	coord_x = result['longitude']
	coord_y = result['latitude']

	return [eval(coord_x), eval(coord_y)]

for line in f:
	if counter%500 == 0:
 
		jobj = json.loads(line)
	
		t = datetime.fromtimestamp(jobj['ts'])
	
		geo = ip_geo(jobj['ip'])

		csv.writer(g).writerow([t, geo[0], geo[1]])
		counter += 1
	else:
		counter += 1
		continue 

f.close()
g.close()

print counter
