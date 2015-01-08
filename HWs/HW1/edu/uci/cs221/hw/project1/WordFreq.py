"""
Homework 2 of CS 221 Information Retrieval.

Author: Varad Meru <vmeru@ics.uci.edu>
Last Change: Jan 7, 2015
Course Webpage: http://www.ics.uci.edu/~lopes/teaching/cs221W15/#homework
Homework Number: 1
Question Number: Part B
"""

__author__ = 'varadmeru'

from collections import Counter


class WordFreq:
    def __init__(self):
        self

    def compute_word_freq(self, token_list):
        lower_token_list = map(lambda word: str(word).lower(), token_list)
        grouped_values = Counter(lower_token_list)
        grouped_sorted_values = sorted(grouped_values.items(), key=lambda x: x[1], reverse=True)
        return grouped_sorted_values

    def print_tokens(self, token_pairs):
        for i in token_pairs:
            print i[0], ",", i[1]