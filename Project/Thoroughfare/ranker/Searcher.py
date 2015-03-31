__author__ = 'varadmeru'

from Ranker import Result
from queryparser.FinderQueryParser import FinderQueryParser
from data.CassandraManager import CassandraManager

import redis
from collections import OrderedDict
from collections import Counter
import re
import math

## Redis initializations
client_id_page_rank = redis.StrictRedis(host='localhost', port=6379, db=15)
client_id_url = redis.StrictRedis(host='localhost', port=6379, db=14)
client_url_index = redis.StrictRedis(host='localhost', port=6379, db=13)
client_id_title = redis.StrictRedis(host='localhost', port=6379, db=12)
client_title_index = redis.StrictRedis(host='localhost', port=6379, db=11)
client_url_id = redis.StrictRedis(host='localhost', port=6379, db=10)


# qparser = FinderQueryParser()


class Searcher:
    """

    """

    def __init__(self):
        """

        :return:
        """
        self.none_result = Result()
        self.result = []

    def search(self, query):
        C = CassandraManager()
        self.result = []
        ## Term Manipulation
        # term = raw_input()
        term1 = query
        term_words = re.findall(r'\w+', term1)
        words = []
        for word in term_words:
            if len(word) != 1:
                words.append(word.lower())
        term = ' '.join(words)
        # term = ' '.join(term.lower().split())
        ## Splitting to words
        # words = term.split()
        words = list(set(words))
        ## Inv Index
        res_tf_idf_map = C.get_inv(term)

        res_inv_ids = res_tf_idf_map.keys()
        ## Term-wise Inverted Index
        res_part_inv_ids_map = C.get_part_inv(words)
        res_part_inv_ids = []

        for i in range(len(words)):
            res_part_inv_ids.append(res_part_inv_ids_map[i].keys())

        # res_part_inv_ids = res_part_inv_ids_map.keys()
        ## Titles Index
        (res_til_ids, res_til_part_ids) = C.get_til(term, words)
        ## Urls Index
        res_url_ids = C.get_url(term)

        ## Set Making
        res = set(res_inv_ids)
        if res_til_ids != None:
            res = res | set(res_til_ids)
        if res_url_ids != None:
            res = res | set(res_url_ids)
        if res_til_part_ids != None:
            res = res | set(res_til_part_ids)
        for i in range(len(words)):
            res = res | set(res_part_inv_ids[i])
        res = list(res)

        ## Unique-ing
        ids = []
        urlsbef = []
        for x in res:
            xurl = client_id_url.get(x)
            urlsbef.append(xurl)
        for i in range(len(res)):
            x = res[i]
            xurl = urlsbef[i]
            ## Domain Check
            if xurl == None or xurl.find(".ics.uci.edu") == -1 or xurl.find("vcp.") != -1 or xurl.find(
                    "ngs.") != -1 or xurl.find("eppstein") != -1:
                continue
            ## https Check
            parts2 = xurl.split(':')
            if parts2[0] == "https":
                url2 = 'http:' + parts2[1]
                if url2 in urlsbef:
                    continue

            ## /index and /index.html Check
            parts3 = xurl.split("/")
            l3 = len(parts3) - 1
            if parts3[l3] == '':
                parts3 = parts3[0:l3]
                l3 -= 1
            if parts3[l3] == 'index' or parts3[l3] == 'index.html':
                parts3 = parts3[0:l3]
                url3 = '/'.join(parts3)
                if url3 in urlsbef or (url3 + '/') in urlsbef:
                    continue

            ## .php Check
            parts = xurl.split('.')
            if parts[len(parts) - 1] != 'php':
                ids.append(int(client_url_id.get(xurl)))
                # urls.append(xurl)

        res = list(set(ids))

        ## Normalized Scoring
        sc_map = {}
        pr_max = 590
        if len(res_tf_idf_map) > 0:
            i, timax = max(res_tf_idf_map.items())
        else:
            i, timax = 0, 1
        i = 0

        sc = [[0 for j in range(6)] for k in range(len(res))]
        for x in res:
            page_rank = client_id_page_rank.get(x)
            sc_map[x] = 0.0

            ## Page Rank
            if page_rank != None:
                sc_map[x] += 0.0 + float(page_rank) / pr_max / 0.75
            sc[i][0] = sc_map[x]
            # print x, sc[i][0], page_rank

            ## Absolute TFIDF
            if len(res_tf_idf_map) > 0 and x in res_tf_idf_map.keys():
                sc_map[x] += res_tf_idf_map[x] / timax / 3
                # sc_map[x] += 1
            sc[i][1] = sc_map[x] - sc[i][0]

            ## Title
            if res_til_ids != None and x in res_til_ids:
                sc_map[x] += 1.2
            sc[i][2] = sc_map[x] - sc[i][1]

            ## Part_Title
            if res_til_part_ids != None and x in res_til_part_ids and sc[i][2] == 0:
                sc_map[x] += 0.45
            sc[i][3] = sc_map[x] - sc[i][2]

            ## URL
            if res_url_ids != None and x in res_url_ids:
                # if sc[i][3] == 0 and sc[i][2] == 0:
                # sc_map[x] += 0.6
                # elif sc[i][3] == 0:
                #     sc_map[x] += 0.2
                # else:
                sc_map[x] += 0.1
            sc[i][4] = sc_map[x] - sc[i][3]

            ## Cosine Similarity
            cs = 0.0
            norm = 0.0
            for j in range(len(words)):
                val = res_part_inv_ids_map[j][x]
                cs += val
                norm = (val * val)
            if norm != 0 and sc[i][1] == 0:
                sc_map[x] += cs / math.sqrt(norm) / len(words)
            sc[i][5] = sc_map[x] - sc[i][4]
            i += 1

        sc_map = OrderedDict(sorted(sc_map.items(), key=lambda t: -t[1]))
        res = sc_map

        ## Temporary printing
        # urls = []
        # titles = []
        diff = 15
        lim = 0
        for x in res:
            if lim == 0:
                prev_sc = sc_map[x]
            if lim > 21:
                break
            if lim > 0:
                diff = prev_sc - sc_map[x]
                prev_sc = sc_map[x]

            if diff > 0:
                res1 = Result()
                res1.title = client_id_title.get(x)
                res1.title = unicode(res1.title, errors='replace')
                res1.url = client_id_url.get(x)
                #urls.append(client_id_url.get(x))
                #titles.append(client_id_title.get(x))
                res1.text = C.get_page_text(x, term, words)
                #res1.text = unicode(C.get_page_text(x,term,words), errors='ignore')
                res1.score = sc_map[x]
                #print sc_map[x], x, client_id_url.get(x), client_id_title.get(x)
                self.result.append(res1)
                lim += 1

        return self.result


'''
COPY finder_keyspace.inverted_index (token_text, collection_freq, count_map, idf, tfidf_map) FROM '/Users/varadmeru/uci-related/uci-courses/CS-221-Information-Retrieval/two_grams.txt'

COPY finder_keyspace.pagerank_urls (url_id, pagerank) FROM '/Users/varadmeru/uci-related/uci-courses/CS-221-Information-Retrieval/pagerank.txt'
'''