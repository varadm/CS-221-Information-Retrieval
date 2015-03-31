import redis
from collections import Counter
import re

pr_client = redis.StrictRedis(host='localhost', port=6379, db=13)
stop_words = ['http','https','ics','uci','edu','www']
SC = Counter(stop_words)
f = open('id_url.txt', 'r')
index = {}
t = 0
for line in f:
##    t += 1
##    if t>=21:
##        break
    val = line.split(',')
    v1 = int(val[0])
    v2 = val[1].strip()
    terms = re.findall(r'\w+',v2)
    terms = [x.lower() for x in terms]
    terms = list(set(terms))
    for term in terms:
        if SC[term] == 0:
            if term in index: index[term] = index[term] + ',' + str(v1)
            else: index[term] = str(v1)
    #pr_client.set(v1, v2)
    #print 'Done for ' + str(v1) + ' ' + v2
##
##print index

for term in index.keys():
    print 'Done for ' + str(v1)
    v1 = term
    v2 = index[term]  
    pr_client.set(v1, v2)

