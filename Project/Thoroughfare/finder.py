#!flask/bin/python
"""
"""

from flask import Flask, render_template, request, url_for
from ranker.Searcher import Searcher

app = Flask(__name__, static_url_path='')
searcher = Searcher()


@app.route('/')
def form():
    """

    :return:
    """
    return render_template('index.html')


@app.route('/search/', methods=['POST'])
def submit(query_from=None):
    """

    :param query_from:
    :return:
    """
    str_query = request.form['search_term']
    plhterm = str_query
    list_of_results = searcher.search(str_query)
    return render_template('search.html', plh_term=plhterm, mylist=list_of_results)


if __name__ == '__main__':
    app.run(debug=True)