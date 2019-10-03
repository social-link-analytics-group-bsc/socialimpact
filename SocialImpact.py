#!/usr/bin/env python
# coding: utf-8

import PyPDF2
from glob import glob
import os
import re
import nltk

def pdf_pages(dictionary, file):
    
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    n = pdfReader.numPages
    content = []
    for i in range(n):
        pageObj = pdfReader.getPage(i)
        content.append(pageObj.extractText())
        
    dictionary[file] = content
    
    return dictionary

def read_as_list(l, encoding):

    ''' Read file as list '''

    l_ = []
    with open(l, "rt", encoding=encoding) as f:
        l_ = f.read().splitlines()
    return l_

def return_positive(dictionary, f, positive_words, words_re):
    
    for i in dictionary[f]:
        for j in nltk.word_tokenize(i):
            if words_re.search(j):
                print(j)
    
    return 

if '__main__' == __name__:

    files = [y for x in os.walk('./data') for y in glob(os.path.join(x[0], '*.pdf'))]
    positive_words = read_as_list('positive_words.txt', encoding = 'latin-1')
    dictionary, positive_sentences = {}, {}
    words_re = re.compile("|".join(positive_words))

    for i, f in enumerate(files):
        print('N. files left: ' + str(len(files)-i))
        dictionary = pdf_pages(dictionary, f)
        positive_sentences = return_positive(dictionary, f, positive_words, words_re)
