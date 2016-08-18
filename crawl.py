#!/usr/bin/env python2

import urllib2
import bs4

def crawl(next_url, info):
#    try:
		n_soup = bs4.BeautifulSoup(urllib2.urlopen(next_url).read())
		sendtime = n_soup.find(id='SendTime').text
		print ('sendtime=', sendtime)
		cn_resume = n_soup.find(id='Abstract').text
		en_resume = n_soup.find(id='EnAbstract').text
		print ('cn_re=' +  cn_resume)
		print ('en_re=', en_resume)
		print (cn_resume)
#	except:
#		print ('something')

if __name__ == '__main__':
	info = {}
	next_url = 'http://zgdz.eq-j.cn/zgdz/ch/reader/view_abstract.aspx?file_no=20150201&flag=1'
	crawl(next_url, info)
