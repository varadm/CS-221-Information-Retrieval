__author__ = 'varadmeru'

from whoosh.qparser import QueryParser
from whoosh import qparser


class FinderQueryParser:
    """
    The Query Parser for Finder
    """

    def __init__(self):
        """
        The constructor of the class.
        :return:
        """
        self.parser = QueryParser("token", schema=None, group=qparser.OrGroup)

    def parse_query(self, query_from_user):
        """
        The Query is parsed with basic AND/OR operators.

        :param query_from_user: The query from the user. The query could contain AND and OR. The default group is OR
        where the tokens are matched independently.
        :return: It returns query fetched form whoosh.
        :rtype: :class:`whoosh.query.Query`
        """
        return self.parser.parse(query_from_user)