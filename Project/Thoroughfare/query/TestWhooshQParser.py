__author__ = 'varadmeru'

from whoosh.qparser import QueryParser
from whoosh.qparser import OperatorsPlugin
from whoosh import qparser


class QueryParse:
    def __init__(self):
        self.query_parser = QueryParser("token", schema=None, group=qparser.OrGroup)
        self.cp = qparser.OperatorsPlugin(And="&", Or="\|", AndNot="&!", AndMaybe="&~", Not=None)
        self.query_parser.add_plugin(self.cp)

    def parse_query(self, query):
        p = self.query_parser.parse(query)
        print "1", p
        for x in p.children():
            print "2", x
        print "3", p.field()
        print "4", p.has_terms()
        for x in p.tokens():
            print "5", x
        for x in p.terms():
            print "6", x
        for x in p.leaves():
            print "7", x
        print "8", p.normalize()
        print "9", p.all_terms()
        for x in p.all_tokens():
            print "10", x
        print "11", p.__getitem__(0)
        print "12", len(p.all_terms())
        return p


def __main__():
    qp = QueryParse()
    qp.parse_query("Hello | World & Varad")
    print("################")
    res = qp.parse_query("Hello & World")
    print "%%%%%%%%", str(res)



__main__()