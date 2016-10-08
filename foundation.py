
#!/usr/bin/python
# -*- coding: utf8 -*-

import urllib2
from bs4 import BeautifulSoup as soup
import re
import datetime
import random
import MySQLdb
import traceback

ori_url = 'http://fund.eastmoney.com/data/fundrating.html'

html = urllib2.urlopen(ori_url).read()
page = soup(html)
print (page)

