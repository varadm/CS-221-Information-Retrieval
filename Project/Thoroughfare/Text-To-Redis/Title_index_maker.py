import redis
from collections import Counter
import re

pr_client = redis.StrictRedis(host='localhost', port=6379, db=11)
#stop_words = ['http','https','ics','uci','edu','www']
#SC = Counter(stop_words)
f = open('id_title.txt', 'r')
index = {}
t = 0
for line in f:
##    t += 1
##    if t>=20:
##        break
    val = line.split(',')
    v1 = int(val[0])
    v2 = val[1].strip()
    if len(v2) == 0:
        continue
    title_terms = re.findall(r'\w+',v2)
    title_terms = [x.lower() for x in title_terms]
    if len(title_terms) > 1:
        terms_2g = [ title_terms[i] + ' ' + title_terms[i+1] for i in range(len(title_terms)-1)]
        if len(title_terms) > 2:
            terms_3g = [ title_terms[i] + ' ' + title_terms[i+1] + ' ' + title_terms[i+2] for i in range(len(title_terms)-2)]    
            title_terms = title_terms + terms_3g
        title_terms = title_terms + terms_2g
    
    terms = list(set(title_terms))
    for term in terms:
        if term in index: index[term] = index[term] + ',' + str(v1)
        else: index[term] = str(v1)
    #pr_client.set(v1, v2)
    #print 'Done for ' + str(v1) + ' ' + v2
##
            
##print index

##
for term in index.keys():
    print 'Done for *' + str(v1) + '*'
    v1 = term
    v2 = index[term]  
    pr_client.set(v1, v2)

