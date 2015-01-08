"""
Homework 2 of CS 221 Information Retrieval.

Author: Varad Meru <vmeru@ics.uci.edu>
Last Change: Jan 7, 2015
Course Webpage: http://www.ics.uci.edu/~lopes/teaching/cs221W15/#homework
Homework Number: 1
Question Number: Part D
"""

__author__ = 'varadmeru'

from collections import Counter


class PalindromeUtility:
    def __init__(self):
        self

    def get_palindromes(self, token_list):
        palindromes_list = filter(lambda s: s == s[::-1], token_list)
        return palindromes_list

    def find_palindromes_freq(self, token_list):
        palindrome_token_list = self.get_palindromes(token_list)
        grouped_values = Counter(palindrome_token_list)
        grouped_sorted_values = sorted(grouped_values.items(), key=lambda x: x[1], reverse=True)
        return grouped_sorted_values

    def print_tokens(self, token_pairs):
        for i in token_pairs:
            print i[0], ",", i[1]