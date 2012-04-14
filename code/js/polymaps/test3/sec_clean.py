import sys
from unidecode import unidecode
import ast
import time
import simplejson as json
import csv
import urllib2 as urllib
from datetime import *


f = open('data/loggarics/snapshots/scribe-logs_horizonlog_2012-03-14_450.log', 'r')
g = open('data/loggarics/snapshots/timegeo_horizonlog_2012-03-14_450.txt', 'r')	
h = open('data/loggarics/snapshots/secgeo_horizonlog_2012-03-14_450.txt', 'w')

counter = 0 

r = {'type': 'GeometryCollection', 'geometries':[]}

for c in range(1963260):
	diff = json.loads(f.readline())['ts'] - start;
	r['geometries'].append(({'type': 'Point', 'coordinates': csv.reader(g).next()[1:3], "ts" : diff}))
	counter += 1 

h.write(json.dumps(r))



f.close()
g.close()
h.close()

print counter
