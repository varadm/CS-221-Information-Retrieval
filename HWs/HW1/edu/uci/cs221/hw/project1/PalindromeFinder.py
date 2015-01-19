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

'''
The Palindrome Utility class with functions to fetch the palindromes from the passed list of tokens.
'''


class PalindromeUtility:
    def __init__(self):
        self

    '''
    Fetch the single word palindromes.
    '''
    def get_palindromes(self, token_list):
        # Apply the lower map to make sure you do not miss out on the important words due to capitalization.
        lower_token_list = map(lambda word: str(word).lower(), token_list)
        palindromes_list = filter(lambda s: s == s[::-1], lower_token_list)
        return palindromes_list

    '''
    Remove spaces. This function is used in the map in the get_palindromes_phrases() method.
    This function helps in removing the spaces and then comparing the palindromes without any spaces.
     Helps in finding the palindromes which are formed without the punctuations.
    '''
    @staticmethod
    def remove_spaces(s):
        l = s.split()
        output = ""
        for i in l:
            output += i
        return output

    '''
    This fetches the palindromic phrases. It takes the token_list and the parameter 'n' which is used to create n-grams
    from the text and then the palindromes are searched.
    '''
    def get_palindromes_phrases(self, token_list, n):
        lower_token_list = map(lambda word: str(word).lower(), token_list)
        n_gram_palindromes = filter(lambda s: self.remove_spaces(s) == self.remove_spaces(s[::-1]),
                                    self.compute_n_grams(lower_token_list, n, True))
        return n_gram_palindromes

    '''
    Find the frequency of the passed palindromes
    '''
    @staticmethod
    def find_palindromes_freq(palindrome_list):
        grouped_values = Counter(palindrome_list)
        grouped_sorted_values = sorted(grouped_values.items(), key=lambda x: x[1], reverse=True)
        return grouped_sorted_values

    '''
    Compute the n-grams from the passed token_list parameter. The keep_space parameter is used to create the n-grams
    with the spaces or not. Helps in reducing some computation.
    '''
    @staticmethod
    def compute_n_grams(token_list, n, keep_space):
        if n == 1:
            return None
        n_gram_list = []
        lower_token_list = map(lambda word: str(word).lower(), token_list)
        len_of_token_list = len(token_list)

        for i in range(len_of_token_list):
            temp = lower_token_list[i]
            for j in range(1, n):
                if (i + j) < len_of_token_list:
                    # This keep_space can now be deprecated.
                    if keep_space:
                        temp = temp + " " + lower_token_list[i + j]
                    else:
                        temp += lower_token_list[i + j]
                    n_gram_list.append(temp)
        return n_gram_list

    '''
    Print tokens.
    '''
    def print_tokens(self, token_pairs):
        for i in token_pairs:
            print i[0], ",", i[1]