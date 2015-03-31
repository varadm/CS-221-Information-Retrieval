__author__ = 'varadmeru'

from collections import OrderedDict

class Scorer:
    def __init__(self):
        pass

    def get_urls(self, term):
        select_all = "SELECT tfidf_map FROM " + self.CassandraIndex + " where token_text = '" + term + "';"
        rows = self.session.execute(select_all)
        doc_ids = {}
        for user_rows in rows:
            doc_ids = user_rows.tfidf_map;
        if len(doc_ids) == 0:
            return doc_ids, 0, 0, 0

        doc_ids = OrderedDict(sorted(doc_ids.items(), key=lambda t: -t[1]))
        urls = []
        titles = []
        texts = []
        tfidfs = []
        l = 0
        for x in doc_ids.keys():
            l += 1
            if (l > 10):
                break
            stmt = "SELECT url,title,page_text,raw_html FROM " + self.CassandraCorpus + " where url_id = " + str(
                x) + ";"
            rows = self.session.execute(stmt)
            for user_rows in rows:
                url = user_rows.url
                title = user_rows.title
                text = user_rows.page_text
                pos = text.lower().find(term)
                if pos != -1:
                    text = text.strip()
                    text = text[max(0, pos - 100):pos + 100]
                else:
                    pos = user_rows.raw_html.lower().find(term)
                    if pos == -1:
                        if len(text) != 0:
                            text = text.strip()
                        else:
                            text = user_rows.raw_html.strip()
                        text = text[0:200]
                    else:
                        text = user_rows.raw_html[max(0, pos - 100):pos + 100]
            urls.append(url)
            titles.append(title)
            texts.append(text)
            tfidfs.append(doc_ids[x])

        return urls, titles, texts, tfidfs