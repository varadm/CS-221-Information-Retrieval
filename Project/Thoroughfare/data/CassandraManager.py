__author__ = 'varadmeru'

import redis
from cassandra.cluster import Cluster
from collections import OrderedDict
from collections import Counter

## Redis initializations
client_id_page_rank = redis.StrictRedis(host='localhost', port=6379, db=15)
client_id_url = redis.StrictRedis(host='localhost', port=6379, db=14)
client_url_index = redis.StrictRedis(host='localhost', port=6379, db=13)
client_id_title = redis.StrictRedis(host='localhost', port=6379, db=12)
client_title_index = redis.StrictRedis(host='localhost', port=6379, db=11)
client_url_id = redis.StrictRedis(host='localhost', port=6379, db=10)

class Cassandra_Config:

    def __init__(self):
        self.CassandraHost = "localhost"
        self.CassandraPort = 9042
        self.CassandraKeyspaceName = "finder_keyspace"

class CassandraManager:

    def __init__(self):
        cfg = Cassandra_Config()
        self.c = Cluster([cfg.CassandraHost], port=cfg.CassandraPort)
        self.session = self.c.connect(cfg.CassandraKeyspaceName)
        self.CassandraIndex = 'inverted_index'
        self.CassandraCorpus = 'finder_corpus'

    def get_inv(self,term):
        nullCntr = Counter()
        #words = terms.split()
        select_all = "SELECT tfidf_map FROM " + self.CassandraIndex + " where token_text = '" + term + "';"
        rows = self.session.execute(select_all)
        doc_ids = {}
        for user_rows in rows:
            doc_ids = user_rows.tfidf_map;
        if len(doc_ids) == 0:
            return nullCntr
        doc_ids = OrderedDict(sorted(doc_ids.items(), key=lambda t: -t[1]))
        return Counter(doc_ids)

    def get_part_inv(self,words):
        nullCntr = Counter()
        result = []
        for term in words:
            select_all = "SELECT tfidf_map FROM " + self.CassandraIndex + " where token_text = '" + term + "';"
            rows = self.session.execute(select_all)
            doc_ids = {}
            for user_rows in rows:
                doc_ids = user_rows.tfidf_map;
            if len(doc_ids) == 0:
                result.append(nullCntr)
                continue
            #doc_ids = OrderedDict(sorted(doc_ids.items(), key=lambda t: -t[1]))
            result.append(Counter(doc_ids))
        return result

    def get_til(self, terms,words):
        ## Individual Words
        result1 = []
        for term in words:
            res = client_title_index.get(term)
            if res == None:
                continue
            temp = res.split(',')
            result = [int(x) for x in temp]
            result1 = result1 + result
        result1 = list(set(result1))

        ## Full query
        term = terms
        res = client_title_index.get(term)
        if res == None:
            return res, result1
        temp = res.split(',')
        result = [int(x) for x in temp]
        return result, result1

    def get_url(self, terms):

        ## Individual Words
        words = terms.split()
        result1 = []
        for term in words:
            res = client_url_index.get(term)
            if res == None:
                continue
            temp = res.split(',')
            result = [int(x) for x in temp]
            result1 = result1 + result
        result1 = list(set(result1))
        return result1

    def get_page_text(self, urlid,term, words):

        stmt = "SELECT page_text,raw_html FROM " + self.CassandraCorpus + " where url_id = " + str(urlid) + ";"
        rows = self.session.execute(stmt)
        for user_rows in rows:
            text = user_rows.page_text
            pos = text.lower().find(term)
            if pos == -1:
                for word in words:
                    pos = text.lower().find(word)
                    if pos != -1:
                        break

            if pos != -1:
                text = text.strip()
                text = text[max(0,pos-100):pos+100]
            else:
                pos = user_rows.raw_html.lower().find(term)
                if pos == -1:
                    for word in words:
                        pos = user_rows.raw_html.lower().find(word)
                        if pos != -1:
                            break

                if pos==-1:
                    if len(text) != 0:
                        text = text.strip()
                    else:
                        text = user_rows.raw_html.strip()
                    text = text[0:200]
                else:
                    text = user_rows.raw_html[max(0,pos-100):pos+100]
            return text
