#!/usr/bin/python
# -*- coding: utf8 -*-

from urllib2 import urlopen
from bs4 import BeautifulSoup as soup
from collections import OrderedDict
import re
import string

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


html = urlopen("https://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = soup(html)
content = bsObj.find("div", {"id": "mw-content-text"}).get_text()
#print("content: " + content.encode("utf8"))
ngrams = ngrams(content, 2)
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t:t[1], reverse=True))
print(ngrams)
print("2-ngrams count is: " + str(len(ngrams)))
