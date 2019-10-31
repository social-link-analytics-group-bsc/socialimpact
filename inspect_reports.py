#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys
import nltk
from glob import glob

def read_as_list(l, encoding):
    l_ = []
    with open(l, "rt", encoding=encoding) as f:
        l_ = f.read().splitlines()
    return l_

def query_yes_no(question, default="yes"):

    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

    return choice

def return_positive(file, positive_words):

    text = re.sub(r'  ', r' ', re.sub(r'[^\x00-\x7f]', r' ', ' '.join(read_as_list(file, 'latin-1'))))

    positive_sentences = []
    for i in nltk.sent_tokenize(text):
        if positive_words in i:
            print(i)
            print('\n')
            answer = query_yes_no("Is this text about impact?")
            if answer:
                f = open("report.sentences", "a+")
                f.write(i)
                f.write("\n")
                f.close()
                
if '__main__' == __name__:

    print("Searching for evidences of impact on text...")
    files = [y for x in os.walk('./data/') for y in glob(os.path.join(x[0], '*.txt'))]
    positive_words = 'impact'
    for i, file in enumerate(files):
        print('\n')
        print('Analyzing ' + str(file))
        print('--------------------------------')
        print('\n')
        return_positive(file, positive_words)
