from cassandra.cluster import Cluster
from collections import Counter
import re

import time

current_milli_time = lambda: int(round(time.time() * 1000))

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost",
             "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount",
             "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as",
             "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
             "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but",
             "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail",
             "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere",
             "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few",
             "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found",
             "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
             "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself",
             "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it",
             "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
             "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my",
             "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none",
             "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
             "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part",
             "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
             "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
             "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take",
             "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter",
             "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this",
             "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top",
             "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via",
             "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter",
             "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who",
             "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you",
             "your", "yours", "yourself", "yourselves", "the"]

SC = Counter(stopwords)


class Config:
    def __init__(self):
        # Cassandra Configurations
        self.CassandraHost = "localhost"
        self.CassandraPort = 9042
        self.CassandraKeyspaceName = 'probe_keyspace'
        self.CassandraURLTable = 'probe_urls'
        self.CassandraCorpusTable = 'probe_corpus_v3'


def srtitm(item):
    return item[1]


def ret_sub_domain(S):
    c = 0
    for i in range(0, len(S)):
        x = S[i]
        if x == '/':
            c += 1

        if c == 3:
            break
    return S[0:(i + 1)]


def clip_proto(S):
    pos = S.find('/')
    return S[(pos + 1):len(S)]


def no_of_words(S):
    X = re.findall(r'\w+', S)
    return len(X)


# def word_cnt(S):
# X = re.findall(r'\w+', S)
# X = [x.lower() for x in X]
# C = Counter(X)
#     sts = list(set(X) & set(stopwords))
#     for x in sts:
#         C[x] = 0
#     return C

def get_words(S):
    X = re.findall(r'\w+', S)
    X2 = map(lambda word: str(word).lower(), X)
    return X2


def get_2grams(S):
    X = re.findall(r'\w+', S)
    X2 = map(lambda word: str(word).lower(), X)
    X2 = [X2[i] + ' ' + X2[i + 1] for i in range(len(X) - 1)]
    return X2


def get_2g_words(S):
    X = re.findall(r'\w+', S)
    X2 = map(lambda word: str(word).lower(), X)
    X2 = [X2[i] + ' ' + X2[i + 1] for i in range(len(X) - 1) if SC[X2[i]] == 0 and SC[X2[i + 1]] == 0]
    return X2


def word_cnt(X):
    X2 = map(lambda word: str(word).lower(), X)
    # X = [x.lower() for x in X]
    C = Counter(X2)
    return C.items()


def two_word_cnt(S):
    X = re.findall(r'\w+', S)
    twogs = [X[i].lower() + ' ' + X[i + 1].lower() for i in range(len(X) - 1) if
             (X[i].lower() not in stopwords) and (X[i + 1].lower() not in stopwords)]
    C = Counter(twogs)
    return C


class CassandraManager:
    """
    The connection into Cassandra would be made in the constructor and the singleton would be maintained here.
    """

    select_count = 'SELECT count(*) FROM probe_keyspace.probe_corpus_v3;'
    select_all = 'SELECT * FROM probe_keyspace.probe_corpus_v3;'
    select_text = 'SELECT text FROM probe_keyspace.probe_corpus_v3;'


    def __init__(self):
        cfg = Config()
        self.c = Cluster([cfg.CassandraHost], port=cfg.CassandraPort)
        self.session = self.c.connect(cfg.CassandraKeyspaceName)

    def no_print_urls(self):
        rows = self.session.execute(self.select_count)
        count = 0
        for user_row in rows:
            count = user_row.count

        print count

    def no_sub_domains(self):
        start = current_milli_time()
        rows = self.session.execute(self.select_all)
        urls = []
        for user_row in rows:
            urls.append(user_row.url)
        domains = map(ret_sub_domain, urls)
        counted_domains = Counter(domains)
        sorted_counted_domains = sorted(counted_domains.items(), key=lambda x: x[1], reverse=True)
        print sorted_counted_domains
        print 'Time takes: ', current_milli_time() - start

    def no_sub_domains1(self):
        start = current_milli_time()
        rows = self.session.execute(self.select_all)
        UC = Counter()
        for user_row in rows:
            UC[ret_sub_domain(user_row.url)] += 1
        sorted_sd = sorted(UC.items(), key=lambda x: clip_proto(x[0]), reverse=False)
        for subdomain in sorted_sd:
            print subdomain
        print 'Time takes: ', current_milli_time() - start

    '''
    def max_page(self):
        rows = self.session.execute('SELECT * FROM probe_keyspace.probe_corpus;')
        urls = []
        ans = ''
        mx = 0
        for user_row in rows:
            ur = user_row.url
            if ur not in urls:
                urls.append(ur)
                ln = no_of_words(user_row.text)
                if ln > mx:
                    mx = ln
                    ans = ur
        print ans
    '''

    def max_page(self):
        start = current_milli_time()
        rows = self.session.execute(self.select_all)
        ans = ''
        mx = 0
        for user_row in rows:
            ln = no_of_words(user_row.text)
            if ln > mx:
                mx = ln
                ans = user_row.url
        print ans, " # of words: ", mx
        print 'Time takes: ', current_milli_time() - start

    # def five_hundred(self):
    #     start = current_milli_time()
    #     rows = self.session.execute('SELECT * FROM probe_keyspace.probe_corpus;')
    #     urls = []
    #     Cntr = Counter()
    #     for user_row in rows:
    #         ur = user_row.url
    #         if ur not in urls:
    #             urls.append(ur)
    #             Cntr = Cntr + word_cnt(user_row.text)
    #     res = sorted(Cntr.items(), reverse=True, key=srtitm)
    #     for i in range(min(len(res), 500)):
    #         print res[i][0], res[i][1]
    #     print 'Time takes: ', current_milli_time() - start

    # def five_hundred(self):
    #     start = current_milli_time()
    #     rows = self.session.execute('SELECT text FROM probe_keyspace.probe_corpus;')
    #     Cntr = Counter()
    #     for user_row in rows:
    #         Cntr = Cntr + word_cnt(user_row.text)
    #     for x in stopwords:
    #         C[x] = 0
    #
    #     res = sorted(Cntr.items(), reverse=True, key=lambda x: x[1])
    #     for i in range(min(len(res), 500)):
    #         print res[i][0], res[i][1]
    #     print 'Time takes: ', current_milli_time() - start

    def five_hundred(self):
        start = current_milli_time()
        rows = self.session.execute(self.select_text)
        text = []
        for user_row in rows:
            text.append(user_row.text)
        u = map(get_words, text)
        l1 = []
        #print 'Number of Docs-', len(u)
        for i in range(len(u)):
            l1 += u[i]
        #print 'Complete # of words- ', len(l1)
        result = Counter(l1)
        #print 'B4 Stopwords-', len(result.items())
        for x in stopwords:
            result[x] = 0
        #print 'After Stopwords-', len(result.items())
        res = sorted(result.items(), reverse=True, key=lambda x1: x1[1])
        for i in range(min(len(res), 500)):
            print res[i][0], res[i][1]
        print 'Time takes: ', current_milli_time() - start

    def twenty(self):
        start = current_milli_time()
        rows = self.session.execute(self.select_text)
        text = []
        for user_row in rows:
            text.append(user_row.text)
        two_grams = map(get_2g_words, text)
        l1 = []
        #print 'Number of Docs-', len(two_grams)
        for i in range(len(two_grams)):
            l1 += two_grams[i]
        #print 'Complete # of words- ', len(l1)
        result = Counter(l1)
        #print 'B4 Stopwords-', len(result.items())
        # for x in stopwords:
        #      result[x] = 0
        # print 'After Stopwords-', len(result.items())
        res = sorted(result.items(), reverse=True, key=lambda x1: x1[1])
        for i in range(min(len(res), 20)):
            print res[i][0], res[i][1]
        print 'Time takes: ', current_milli_time() - start


C = CassandraManager()

print '=================================================================='
print 'C.no_print_urls()'
## Answer 2
C.no_print_urls()
print '************************************************************************'

print '=================================================================='
print 'C.no_sub_domains()'
## Answer 3
C.no_sub_domains1()
print '************************************************************************'

print '=================================================================='
print 'C.max_page()'
## Answer 4
C.max_page()
print '************************************************************************'

print '=================================================================='
print 'C.five_hundred()'
## Answer 5
C.five_hundred()
print '************************************************************************'

print '=================================================================='
print 'C.twenty()'
## Answer 6
C.twenty()
print '************************************************************************'