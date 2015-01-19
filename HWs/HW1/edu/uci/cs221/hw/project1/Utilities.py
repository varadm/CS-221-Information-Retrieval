"""
Homework 2 of CS 221 Information Retrieval.

Author: Varad Meru <vmeru@ics.uci.edu>
Last Change: Jan 7, 2015
Course Webpage: http://www.ics.uci.edu/~lopes/teaching/cs221W15/#homework
Homework Number: 1
Question Number: Part A


Reference for REGEX usage
http://chimera.labs.oreilly.com/books/1230000000393/ch02.html

"""

__author__ = 'varadmeru'

import re


class Utilities:
    def __init__(self):
        self

    '''
    Tokenize function. This tokenizes the file into words, ignoring the Capital words in them.
    '''
    def tokenize_file(self, filename):

        return_list = []
        f = open(filename)

        lines = f.readlines()
        f.close()

        # For each line -
        for line in lines:
            # Checking for standard delimiters such as ';',',','*','.',' '
            # For some advanced symbols, you'll add more stuff into reg.
            l = re.split(r"[\W_]+", line)

            # Filtering the empty strings from the list.
            l2 = filter(lambda q: str(q).lstrip('-'), l)
            l3 = filter(None, l2)
            l4 = filter(lambda q: str(q).rstrip('-'), l3)
            l5 = filter(None, l4)

            # Now, once the words are cleaned and parsed, add them to the return_list
            return_list.extend(l5)

        return return_list

    '''
    Print tokens.
    '''
    def print_tokens(self, token_list):
        for token in token_list:
            print token


'''
Some Important Cases:
1. Currently everything is being converted into lowercase. But this is not the correct way
to store info, as there can be a single ACRONYM and that would also be made into lower case.
Thus, its important to know what data is already in the list/set/map and leverage that.

2. What if you have Apple and APPLE?

3. Most punctuation is ignored by Google. Which punctuation to keep into account while tokenzing.
'''