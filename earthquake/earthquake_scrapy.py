#!/usr/bin/env python2

'''
 **********************************************************
 * Author        : Feng.Wei
 * Email         : alferwei98@163.com
 * Last modified : 2016-08-17 16:35
 * Filename      : earthquake_scrapy.py
 * Description   : 
 * *******************************************************
'''

import urllib2
import bs4
import re
from datetime import datetime
from elasticsearch import Elasticsearch

base_url = 'http://zgdz.eq-j.cn/zgdz/ch/'
request_url = 'http://zgdz.eq-j.cn/zgdz/ch/index.aspx'

response_data = urllib2.urlopen(request_url)
page = response_data.read()
#print ("page=%s" %(page))

soup = bs4.BeautifulSoup(page)
#links = soup.select('a[href^="reader/view_abstract.aspx"]')
links = soup.select("ul")
#print ("links=%s" %(links))

es = Elasticsearch("cstor02:9200")

def crawl(next_url, info):
	try:
		n_soup = bs4.BeautifulSoup(urllib2.urlopen(next_url).read())
		sendtime = n_soup.find(id="SendTime")
		print ('sendtime=', sendtime)
	except:
		print ('something')

urls = []
for link in links:
	print ("===============================")
	#print ("link=%s" %(link))
	titlel = link.select(".title")
	authorl = link.select(".author")
	info = {}
	if (len(titlel) > 0):
		title = titlel[0]	
		url = title.a["href"]
		author = authorl[0].get_text()
		#print("********* title=%s" %(title.a["href"]))
		#href = info["href"].find_all(re.compile(r"flag=1$"))
		#print (info["href"])
		if re.match(r'.*flag=1$', url):
			try:
				name = title.a['title']
				if name:
					next_url = base_url + url
					#crawl(next_url, info)
					info['url'] = url
					info['title'] = title.a['title']
					info['author'] = author
					timel = link.select(".time")
					if (len(timel) > 0):
						time = timel[0].get_text()
						info['time'] = time.strip()[-10:]
					else: 
						info['time'] = '1970-01-01'
					#urls.append(info)
					obj = {"url":info['url'],"title":info['title'],"author":info['author'],"time":info['time'],"timestamp":datetime.now()}
					es.index(index="scrapy-index", doc_type="test-type", body=obj)
					print ("***info***=%s" %(info))
			except KeyError,e:
				print ('KeyError: ', e)	
				continue
		else:
			print ('url is not satisfied')
			continue
	else:
		print ("titlel is null")
		continue

# print ("urls=%s" %(urls))
