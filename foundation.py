#!/usr/bin/env python2

import urllib2
from bs4 import BeautifulSoup as soup
import re
import datetime
import random
import MySQLdb
import traceback


src_url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=06%2C07%2C08&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=03&cotype=99&degreefrom=99&jobterm=99&companysize=03%2C05%2C06%2C07%2C04&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9"
urlP = "(https:)*//jobs\.51job\.com/nanjing.*.*$"
pages = set()
random.seed(datetime.datetime.now())

conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='root',db ='scrapy', use_unicode=True, charset="utf8")
cur = conn.cursor()

def crawl(surl, pattern):
	html = urllib2.urlopen(surl).read()
	page = soup(html)
	urls = page.findAll("a", href=re.compile(pattern))
	print urls


if __name__ == "__main__":
	crawl(src_url, urlP)

