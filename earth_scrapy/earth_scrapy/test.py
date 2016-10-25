#!/usr/bin/env python2

import urllib2
import bs4

def crawl(next_url, info):
#    try:
		n_soup = bs4.BeautifulSoup(urllib2.urlopen(next_url).read())
		journal = n_soup.findAll('table', {'class':"front_table"})
		print ("journal=%s" %(journal))
#	except:
#		print ('something')

if __name__ == '__main__':
	info = {}
	next_url = 'http://zgdz.eq-j.cn/zgdz/ch/reader/view_abstract.aspx?file_no=20110401&flag=1'
	crawl(next_url, info)
