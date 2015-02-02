"""
Homework 2 of CS 221 Information Retrieval.

Author: Varad Meru <vmeru@ics.uci.edu>
Last Change: Jan 7, 2015
Course Webpage: http://www.ics.uci.edu/~lopes/teaching/cs221W15/#homework
Homework Number: 1

This module tests the code.
"""

from Utilities import Utilities
from WordFreq import WordFreq
from TwoGrams import TwoGram
from PalindromeFinder import PalindromeUtility

import time

__author__ = 'varadmeru'

'''
TEST the 4 classes.
'''

# Sample Text files -
# Work of Sherlock
f1 = "pg100.txt"

# Sample handwritten text file
f2 = "helloworld.txt"

# Sherlock in text
f3 = "sherlock.txt"

#
f4 = "vendlist.txt"

# Sherlock in text
f5 = "sherlock1.txt"

# Test 1
f6 = "test1.txt"

# Test 2
f7 = "test3.txt"

sample_file = f1

current_milli_time = lambda: int(round(time.time() * 1000))


def test_util():
    x = Utilities()
    answer = x.tokenize_file(sample_file)
    x.print_tokens(answer)
    print "Number of tokens: ", len(answer)


def test_wordfreq():
    x = Utilities()
    y = WordFreq()
    answer = x.tokenize_file(sample_file)
    i = y.compute_word_freq(answer)
    #y.print_tokens(i)
    print "Number of distinct: ", len(i)


def test_2grams():
    x = Utilities()
    z = TwoGram()
    answer = x.tokenize_file(sample_file)
    i = z.compute_2grams_freq(answer)
    #z.print_tokens(i)
    print "Number of 2 grams:", len(i)


def test_palindrome_finder():
    x = Utilities()
    y = PalindromeUtility()
    answer = x.tokenize_file(sample_file)
    palindromes = y.get_palindromes(answer)
    palindromes.extend(y.get_palindromes_phrases(answer, 50))
    i = y.find_palindromes_freq(palindromes)
    #y.print_tokens(i)
    print "Number of distinct palindromes: ", len(i)


def __main__():
    start = current_milli_time()

    current = current_milli_time()
    # Testing the utilities
    test_util()
    print "+++ Time taken for utility.py: ", current_milli_time() - current

    current = current_milli_time()
    # Testing the word freq
    test_wordfreq()
    print "+++ Time taken for word_freq.py: ", current_milli_time() - current


    current = current_milli_time()
    # Testing the word freq
    test_2grams()
    print "+++ Time taken for 2grams.py: ", current_milli_time() - current

    current = current_milli_time()
    # Testing the word freq
    test_palindrome_finder()
    print "+++ Time taken for word_freq.py: ", current_milli_time() - current

    print "-----------------------------------"
    print "+++ Total Time taken: ", current_milli_time() - start

__main__()


'''
Some Notes:
For the pg100.txt file - Time taken:  46257 for n = 15
For the pg100.txt file - Time taken:  13691 for n = 6
'''