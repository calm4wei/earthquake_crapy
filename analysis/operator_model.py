#!/usr/bin/python
# -*- coding: utf8 -*-

from urllib2 import urlopen
from bs4 import BeautifulSoup as soup
import re
import string
import operator

def cleanInput(input):
    input = re.sub('\n+'," ",input)
    input = re.sub(' +'," ",input)
    input = input.encode("utf8")
    input = input.split(' ')
    cleanData = []
    for item in input:
        # string.punctuation 去除特殊字符
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanData.append(item)
    return cleanData

def ngrams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input) - n + 1):
        ngramTemp = " ".join(input[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
                   "they", "is", "an", "at", "but","we", "his", "from", "that", "not", "by", "she", "or", "as", "what", "go", "their","can", "who",
                   "get", "if", "would", "her", "all", "my", "make", "about", "know", "will","as", "up", "one", "time", "has", "been", "there",
                   "year", "so", "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see", "him", "your",
                   "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "more", "these", "want", "way", "look",
                   "first", "also", "new", "because", "day", "more", "use", "no", "man", "find", "here", "thing", "give", "many", "well"]
    for word in ngram:
        if word in commonWords:
            return True
        return False

content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read())
ngrams = ngrams(content,2)
sortedNGrams = sorted(ngrams.items(), key=operator.itemgetter(1),reverse=True)
print(sortedNGrams)



