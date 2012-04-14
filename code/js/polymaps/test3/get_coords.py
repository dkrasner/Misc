import urllib
import sys
from unidecode import unidecode
import ast
import time
import simplejson as json
import csv

f = open('zip_764.txt', 'r')
g = open('coordinates.json', 'w')

bad=0

def get_coords(zipcode):
	
	#query = "http://maps.googleapis.com/maps/api/geocode/json?address=" + str(zipcode) + "&sensor=false" #google
 	query = "http://where.yahooapis.com/geocode?location=" + str(zipcode) + "&flags=J&appid=rA6YE3nV34HPRkTJdWvcgser3lUoB2iMtD0_NWePIM20_X1GYbgStJVYVO3tWRc-"   #yahoo	
	
	result = ast.literal_eval(urllib.urlopen(query).read())
	
	#coord_x = result['results'][0]['geometry']['location']['lng'] #google
	#coord_y = result['results'][0]['geometry']['location']['lat']

	coord_x = result['ResultSet']['Results'][0]['longitude']  #yahoo
	coord_y = result['ResultSet']['Results'][0]['latitude']
 
	
	return [float(coord_x), float(coord_y)]



r = {'type': 'GeometryCollection', 'geometries':[]}

for i in range(25000):
	try:
		r['geometries'].append(({'type': 'Point', 'coordinates': get_coords(csv.reader(f).next()[0])}))
		print get_coords(csv.reader(f).next()[0])
	except:
		bad +=1
g.write(json.dumps(r))

print 'bad= ' + str(bad)
print 'yahoo request left: ' + str(urllib.urlopen('http://ydntest.com/limitcalculator/?output=json&callback=foo').read())


	
