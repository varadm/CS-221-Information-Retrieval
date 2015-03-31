__author__ = 'varadmeru'


class Result:
    """

    """
    title = ""
    text = ""
    url = ""
    score = ""

    def __init__(self, title="Template Title", text="Random Text", url="http://www.ics.uci.edu", score=1.000):
        """
        :return:
        """
        self.title = title
        self.text = text
        self.url = url
        self.score = score

    def new_result(self, title, text, url, score):
        """

        :param title:
        :param text:
        :param url:
        :param score:
        :return:
        """
        self.title = title
        self.text = text
        self.url = url
        self.score = score
        return self


class Ranker:
    """

    """

    def __init__(self):
        pass