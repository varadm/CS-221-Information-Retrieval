from cassandra.cluster import Cluster
from collections import Counter
import re

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

class Config:
    def __init__(self):

        # Cassandra Configurations
        self.CassandraHost = "localhost"
        self.CassandraPort = 9042
        self.CassandraKeyspaceName = 'probe_keyspace'
        self.CassandraURLTable = 'probe_urls'
        self.CassandraCorpusTable = 'probe_corpus'

def srtitm(item):

    return item[1]

def ret_sub_domain(S):
    c = 0
    for i in range(0, len(S)):
        x = S[i]
        if x == '/':
            c+=1

        if c==3:
            break
    return S[0:(i+1)]

def no_of_words(S):
    X = re.findall(r'\w+',S)
    return len(X)

def word_cnt(S):   
    X = re.findall(r'\w+',S)
    X = [x.lower() for x in X]
    C = Counter(X)
    sts = list(set(X) & set(stopwords))   
    for x in sts:
        C[x] = 0
    return C

def two_word_cnt(S):   
    X = re.findall(r'\w+',S)
    twogs = [X[i].lower() + ' ' +  X[i+1].lower() for i in range(len(X)-1) if (X[i].lower() not in stopwords) and (X[i+1].lower() not in stopwords)]
    C = Counter(twogs)
    return C

class CassandraManager:
    """
    The connection into Cassandra would be made in the constructor and the singleton would be maintained here.
    """

    def __init__(self):
        cfg = Config()
        self.c = Cluster([cfg.CassandraHost], port=cfg.CassandraPort)
        self.session = self.c.connect(cfg.CassandraKeyspaceName)

    def no_print_urls(self):
        rows = self.session.execute('SELECT * FROM probe_keyspace.probe_corpus;')
        urls = []
        for user_row in rows:
            if user_row.url not in urls:
                urls.append(user_row.url)

        print len(urls)

    def no_sub_domains(self):
        rows = self.session.execute('SELECT * FROM probe_keyspace.probe_corpus;')
        urls = []
        UC = Counter()
        for user_row in rows:
            ur = user_row.url
            if ur not in urls:
                urls.append(ur)
                UC[ret_sub_domain(ur)] += 1
        print UC.items()

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
                if ln>mx:
                    mx = ln
                    ans = ur
        print ans

    def five_hundred(self):
        rows = self.session.execute('SELECT * FROM probe_keyspace.probe_corpus;')
        urls = []
        Cntr = Counter()
        for user_row in rows:
            ur = user_row.url
            if ur not in urls:
                urls.append(ur)
                Cntr = Cntr + word_cnt(user_row.text)
        res = sorted(Cntr.items(), reverse=True, key=srtitm)
        for i in range(min(len(res),500)):
            print res[i][0],res[i][1]

    def twenty(self):
        rows = self.session.execute('SELECT * FROM probe_keyspace.probe_corpus;')
        urls = []
        Cntr = Counter()
        for user_row in rows:
            ur = user_row.url
            if ur not in urls:
                urls.append(ur)
                Cntr = Cntr + two_word_cnt(user_row.text)
        res = sorted(Cntr.items(), reverse=True, key=srtitm)
        for i in range(min(len(res),20)):
            print res[i][0],res[i][1]

C = CassandraManager()

## Answer 2
C.no_print_urls()

## Answer 3
C.no_sub_domains()

## Answer 4
C.max_page()

## Answer 5
C.five_hundred()

## Answer 6
C.twenty()
