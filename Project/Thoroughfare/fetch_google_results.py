from finder import form

__author__ = 'varadmeru'

from pygoogle import pygoogle
from ranker.Searcher import Searcher
# from app_26k import CassandraManager
import math
from operator import truediv

query_list = ['mondego', 'machine learning', 'software engineering', 'security', 'student affairs', 'graduate courses',
              'Crista Lopes', 'REST', 'computer games', 'information retrieval']
site = "site:ics.uci.edu "
searcher = Searcher()


def get_thoroghfare_results():
    print '----------------------------------------'
    for i in query_list:
        print "*** *** QUERY --", i, "*** *** "
        list_of_results = searcher.search(i)
        print '-----Thoroughfare SEARCH RESULT---------'
        print '----------------------------------------'
        for x in range(len(list_of_results)):
            a = list_of_results.__getitem__(x)
            print a.url
        print '----------------------------------------'


def get_thoroghfare_for_query_results(query):
    print '----------------------------------------'
    list_of_results = searcher.search(query)
    print '-----Thoroughfare SEARCH RESULT---------'
    print '----------------------------------------'
    for x in range(10):
        a = list_of_results.__getitem__(x)
        print a.url
    print '----------------------------------------'


def get_google_query_results():
    for i in query_list:
        print "*** *** QUERY --", i, "*** *** "
        g = pygoogle('machine learning "graduate" "courses" site:ics.uci.edu -ARCHIVE.ICS.UCI.EDU/ml')
        g.pages = 3
        print '----------------------------------------'
        print '--------GOOGLE SEARCH RESULT------------'
        print '----------------------------------------'
        print g.get_urls()[0:10]
        print '----------------------------------------'
        print '\n'


def get_both_results():
    for i in query_list:
        print "*** *** QUERY --", i, "*** *** "
        g = pygoogle(site + i)
        g.pages = 1
        list_of_results = searcher.search(i)
        print '----------------------------------------'
        print '-----Thoroughfare SEARCH RESULT---------'
        print '----------------------------------------'
        for x in range(10):
            a = list_of_results.__getitem__(x)
            print a.url
        print '----------------------------------------'
        print '--------GOOGLE SEARCH RESULT------------'
        print '----------------------------------------'
        print g.get_urls()[0:10]
        print '----------------------------------------'


def compute_dcg(ordered_relevance):
    dcgs = list()
    dcgs.append(ordered_relevance[0])
    for i in range(1, len(ordered_relevance)):
        dcgs.append(ordered_relevance[i] / math.log(i + 1, 2))
    return dcgs


def compute_ndcg(query, user_relevance):
    ideal_relevance_case = [5, 4, 3, 2, 1]
    dcgs_user = compute_dcg(user_relevance)
    dcgs_ideal = compute_dcg(ideal_relevance_case)
    print "NDCG-5 of", query, "is", (sum(dcgs_user) / sum(dcgs_ideal))
    return sum(dcgs_user) / sum(dcgs_ideal)

# get_both_results()
# get_thoroghfare_for_query_results("Crista Lopes")

#get_thoroghfare_results()
# get_thoroghfare_old_results()
# get_google_query_results()
# query = "Machine Learning"
# user_relevance = [3, 2, 0, 1, 4]
# compute_ndcg(query, user_relevance)

# New 2
queries = {'Mondego': [3, 4, 0, 1, 0],
           'Machine Learning': [5, 2, 0, 0, 0],
           'Software engineering': [5,0,0,0,0],
           'Security': [0, 0, 0, 0, 0],
           'Student Affairs': [0, 0, 0, 2, 5],
           'Graduate Courses': [5, 0, 0, 0, 0],
           'Crista Lopes': [5, 2, 0, 0, 1],
           'REST': [5, 3, 0, 0, 0],
           'computer games': [3, 0, 0, 0, 0],
           'information retrieval': [3, 0, 3, 0, 2]}

# queries = {'Mondego': [3, 4, 0, 0, 0],
# 'Machine Learning': [0, 0, 0, 0, 0],
#            'Software engineering': [0, 0, 0, 0, 0],
#            'Security': [0, 0, 0, 0, 0],
#            'Student Affairs': [0, 0, 3, 0, 0],
#            'Graduate Courses': [0, 5, 0, 0, 0],
#            'Crista Lopes': [0, 0, 0, 0, 0],
#            'REST': [5, 3, 4, 1, 2],
#            'computer games': [0, 0, 0, 0, 0],
#            'information retrieval': [0, 0, 0, 4, 0]}

x = 0

for i in queries:
    x += compute_ndcg(i, queries[i])

print
print "Average NDCG is ", x / len(queries)
'''
/usr/local/bin/python /Users/varadmeru/uci-related/uci-courses/CS-221-Information-Retrieval/Thoroughfare-New/Thoroughfare/fetch_google_results.py
NDCG-5 of Crista Lopes is 0.568022024237
NDCG-5 of REST is 0.649168027699
NDCG-5 of Software engineering is 0.405730017312
NDCG-5 of Graduate Courses is 0.0
NDCG-5 of Security is 0.0
NDCG-5 of information retrieval is 0.386405868054
NDCG-5 of Student Affairs is 0.255987139839
NDCG-5 of computer games is 0.342655734546
NDCG-5 of Mondego is 0.608595025968
NDCG-5 of Machine Learning is 0.277133263299
Average NDCG is  0.349369710095

Process finished with exit code 0

/usr/local/bin/python /Users/varadmeru/uci-related/uci-courses/CS-221-Information-Retrieval/Thoroughfare-New/Thoroughfare/fetch_google_results.py
NDCG-5 of Crista Lopes is 0.568022024237
NDCG-5 of REST is 0.527449022506
NDCG-5 of Software engineering is 0.255987139839
NDCG-5 of Graduate Courses is 0.0
NDCG-5 of Security is 0.0
NDCG-5 of information retrieval is 0.284011012118
NDCG-5 of Student Affairs is 0.255987139839
NDCG-5 of computer games is 0.0
NDCG-5 of Mondego is 0.608595025968
NDCG-5 of Machine Learning is 0.0
Average NDCG is  0.250005136451

Process finished with exit code 0


OLD Indexer NDCG v0
NDCG-5 of Crista Lopes is 0.0
NDCG-5 of REST is 0.964426104247
NDCG-5 of Software engineering is 0.0
NDCG-5 of Graduate Courses is 0.405730017312
NDCG-5 of Security is 0.0
NDCG-5 of information retrieval is 0.162292006925
NDCG-5 of Student Affairs is 0.153592283904
NDCG-5 of computer games is 0.0
NDCG-5 of Mondego is 0.568022024237
NDCG-5 of Machine Learning is 0.0

(0.964426104247 + 0.405730017312 + 0.162292006925 + 0.153592283904 + 0.568022024237) / 10 =
Average NDCG for 10 queries: 0.2254062436625

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

New Results - v1
NDCG-5 of Crista Lopes is 0.568022024237
NDCG-5 of REST is 0.792135885366
NDCG-5 of Software engineering is 0.0
NDCG-5 of Graduate Courses is 0.405730017312
NDCG-5 of Security is 0.0
NDCG-5 of information retrieval is 0.0
NDCG-5 of Student Affairs is 0.0
NDCG-5 of computer games is 0.0
NDCG-5 of Mondego is 0.518749299484
NDCG-5 of Machine Learning is 0.0
Average NDCG is  0.22846372264

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Old Ones
queries = {'Mondego': [3, 4, 0, 0, 0],
'Machine Learning': [0, 0, 0, 0, 0],
           'Software engineering': [0, 0, 0, 0, 0],
           'Security': [0, 0, 0, 0, 0],
           'Student Affairs': [0, 0, 3, 0, 0],
           'Graduate Courses': [0, 5, 0, 0, 0],
           'Crista Lopes': [0, 0, 0, 0, 0],
           'REST': [5, 3, 4, 1, 2],
           'computer games': [0, 0, 0, 0, 0],
           'information retrieval': [0, 0, 0, 4, 0]}

# New - 1
# queries = {'Mondego': [0, 4, 3, 1, 0],
#            'Machine Learning': [0, 0, 0, 0, 0],
#            'Software engineering': [0, 0, 0, 0, 0],
#            'Security': [0, 0, 0, 0, 0],
#            'Student Affairs': [0, 0, 0, 0, 0],
#            'Graduate Courses': [5, 0, 0, 0, 0],
#            'Crista Lopes': [5, 2, 0, 0, 0],
#            'REST': [5, 3, 2, 1, 0],
#            'computer games': [0, 0, 0, 0, 0],
#            'information retrieval': [0, 0, 0, 0, 0]}

# New 2
queries = {'Mondego': [0, 4, 3, 1, 0],
           'Machine Learning': [0, 0, 0, 0, 0],
           'Software engineering': [0, 0, 0, 0, 0],
           'Security': [0, 0, 0, 0, 0],
           'Student Affairs': [0, 0, 0, 0, 0],
           'Graduate Courses': [5, 0, 0, 0, 0],
           'Crista Lopes': [5, 2, 0, 0, 0],
           'REST': [5, 3, 2, 1, 0],
           'computer games': [0, 0, 0, 0, 0],
           'information retrieval': [0, 0, 0, 0, 0]}

# New 3
queries = {'Mondego': [0, 4, 3, 1, 0],
           'Machine Learning': [0, 0, 0, 0, 0],
           'Software engineering': [0, 0, 0, 0, 0],
           'Security': [0, 0, 0, 0, 0],
           'Student Affairs': [0, 0, 0, 0, 0],
           'Graduate Courses': [5, 0, 0, 0, 0],
           'Crista Lopes': [5, 2, 0, 0, 0],
           'REST': [5, 3, 2, 1, 0],
           'computer games': [0, 0, 0, 0, 0],
           'information retrieval': [0, 0, 0, 0, 0]}

# New 4
queries = {'Mondego': [3, 4, 0, 1, 0],
           'Machine Learning': [5, 2, 0, 0, 0],
           'Software engineering': [5,0,0,0,0],
           'Security': [0, 0, 0, 0, 0],
           'Student Affairs': [0, 0, 0, 2, 5],
           'Graduate Courses': [5, 0, 0, 0, 0],
           'Crista Lopes': [5, 2, 0, 0, 1],
           'REST': [5, 3, 0, 0, 0],
           'computer games': [3, 0, 0, 0, 0],
           'information retrieval': [3, 0, 3, 0, 2]}

/usr/local/bin/python /Users/varadmeru/uci-related/uci-courses/CS-221-Information-Retrieval/Thoroughfare-New/Thoroughfare/fetch_google_results.py
NDCG-5 of Crista Lopes is 0.602969705709
NDCG-5 of REST is 0.649168027699
NDCG-5 of Software engineering is 0.405730017312
NDCG-5 of Graduate Courses is 0.405730017312
NDCG-5 of Security is 0.0
NDCG-5 of information retrieval is 0.466925657236
NDCG-5 of Student Affairs is 0.255884410825
NDCG-5 of computer games is 0.243438010387
NDCG-5 of Mondego is 0.608595025968
NDCG-5 of Machine Learning is 0.568022024237

Process finished with exit code 0

'''