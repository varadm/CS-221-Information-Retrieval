"""
Homework 2 of CS 221 Information Retrieval.

Author: Varad Meru <vmeru@ics.uci.edu>
Last Change: Jan 7, 2015
Course Webpage: http://www.ics.uci.edu/~lopes/teaching/cs221W15/#homework
Homework Number: 1
Question Number: Part C
"""

__author__ = 'varadmeru'

from collections import Counter


class TwoGram:
    def __init__(self):
        self

    def compute_2grams(self, token_list):
        two_gram_list = []
        len_of_token_list = len(token_list)

        for i in range(len_of_token_list - 1):
            obj1 = token_list[i]
            obj2 = token_list[i + 1]

            obj1 += " " + obj2
            two_gram_list.append(obj1)

        return two_gram_list

    def compute_2grams_freq(self, token_list):
        two_gram_token_list = self.compute_2grams(token_list)
        grouped_values = Counter(two_gram_token_list)
        grouped_sorted_values = sorted(grouped_values.items(), key=lambda x: x[1], reverse=True)
        return grouped_sorted_values

    def print_tokens(self, token_pairs):
        for i in token_pairs:
            print i[0], ",", i[1]