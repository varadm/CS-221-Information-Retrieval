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

__author__ = 'varadmeru'

'''
TEST Utilities
'''

f1 = "pg100.txt"
f2 = "helloworld.txt"
f3 = "sherlock.txt"
s = "Hello, World. world; \"World\" \'world\' .... World world\
What in the world is [100] doing * here.,,as adj ascxs [][ (Hey) co-operate -- whatis---"


def test_util():
    x = Utilities()
    answer = x.tokenize_file(f3)
    # x.print_tokens(answer)
    print len(answer)


def test_wordfreq():
    x = Utilities()
    y = WordFreq()
    answer = x.tokenize_file(f3)
    i = y.compute_word_freq(answer)
    y.print_tokens(i)
    print len(answer)
    print len(i)


def test_2grams():
    x = Utilities()
    z = TwoGram()
    answer = x.tokenize_file(f3)
    i = z.compute_2grams_freq(answer)
    z.print_tokens(i)
    print len(answer)
    print len(i)


def test_palindrome_finder():
    x = Utilities()
    y = PalindromeUtility()
    answer = x.tokenize_file(f3)
    i = y.find_palindromes_freq(answer)
    y.print_tokens(i)
    print len(answer)
    print len(i)


def __main__():
    # test_util()
    # test_wordfreq()
    # test_2grams()
    test_palindrome_finder()


__main__()