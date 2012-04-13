import sys
from numpy import *
from datetime import *
from pymongo import Connection
import csv

def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_subsets(s, k):
    '''
    Yield all subsets of size k from set (or list) s
    s -- a set or list (any iterable will suffice)
    k -- an integer > 0
    '''
    s = list(s)
    n = len(s)
    for k_set in k_subsets_i(n, k):
        yield set([s[i] for i in k_set])





###########Call to cmnd line to enter port, db name, collection name#####


c_id = raw_input("Enter client_id: ")
port = raw_input("Enter port: ")







########The profile DB#########
con = Connection('localhost', int(port))
#con = Connection()
db = con['sailthru']
collection = db['profile.'+str(c_id)]
#collection = db['profile']



###### get a collection of list anmes
lists = collection.distinct("lists")
L = len(lists)



print "done with lists, count: " + str(L)

M = [0]*L
for i in range(L):
	M[i] = [0]*L



counter = 0
badlist = 0

for item in collection.find({"lists": {"$ne": None}}):
	
	ind = []
	
	if len(item['lists']) == 0:
		counter ++ 1
		continue
	
	else:
		for l in item['lists']:
			try:
				ind.append(lists.index(l))	
			except:
				badlist += 1

	if len(ind) == 0:
		counter += 1
		continue
	else:
		for i in k_subsets(ind, 2):
			a = list(i)[0]
			b = list(i)[1]
			M[a][b] += 1
			M[b][a] += 1
	
	counter += 1


print "counter: " + str(counter)
print "badlist: " + str(badlist)
	



