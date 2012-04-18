### this script populates the world.json and states.json files based on user geo data

import simplejson as json




### state and country codes files
f1 = open('code_to_cntry.json', 'r')
f2 = open('code_to_state.json', 'r')
ccntry = json.load(f1)
cstate = json.load(f2)
f1.close()
f2.close()


### border coordinate files
f3 = open('states.json', 'r')
f4 = open('world.json', 'r')
state = json.load(f3)
world = json.load(f4)
f3.close()
f4.close()


### location data
g = open('1074_geo.json', 'r')
geo = json.load(g)
g.close()

#get the total user count
total = 0
for key in geo:
	total += geo[key]['count']

#### clean up keys in geo so that they match those in state and world

geo_use = {}

nokey=0

for key in geo.keys():
	#get the country code
	k = key[(len(key)-2):len(key)]

	if k == 'US':
		sk = key[(len(key)-5):(len(key)-3)]
		state_name = cstate[sk]
		if state_name in geo_use.keys():
			geo_use[state_name] += geo[key]['count']
		else:
			geo_use.update({state_name: geo[key]['count']})
	else:
		try:
			cntry_name = ccntry[k]
			if cntry_name in geo_use.keys():
				geo_use[cntry_name] += geo[key]['count']
			else:
				geo_use.update({cntry_name: geo[key]['count']})
		except:
			nokey += 1
			print key


####populate world.json and state.json with the appropriate region weight (note: thatthis file also contain counts by browser so you can get those weights by asking looking in geo_use[country/state_key]['browsers']['browser_name']

W = len(world['features'])

for i in range(W):
	name = world['features'][i]['properties']['name']
	if name in geo_use.keys():
		weight = geo_use[name]
               # print weight
		world['features'][i]['properties']['q'] = weight
	else:
		world['features'][i]['properties']['q'] = 0

S = len(state['features'])

for i in range(S):
	name = state['features'][i]['properties']['name']
	if name in geo_use.keys():
		weight = geo_use[name]
		#print weight	
		state['features'][i]['properties']['q'] = weight
	else:
		state['features'][i]['properties']['q'] = 0

######dump json into new files
h1 = open('states.json', 'w')
h2 = open('world.json', 'w')
h3 = open('chloro_data.json', 'w')

h1.write(json.dumps(state))
h2.write(json.dumps(world))

#geo_use = {"type": "FeatureCollection", "features": [{key: geo_use[key]} for key in geo_use]}
h3.write(json.dumps(geo_use))

h1.close()
h2.close()
h3.close()





	
