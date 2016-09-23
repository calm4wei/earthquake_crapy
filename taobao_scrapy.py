#!/usr/bin/env python2

import urllib2
import bs4
import re
import datetime
import random
import MySQLdb
import traceback


src_url = "https://weixiaoxiangnuan.taobao.com/?spm=a217f.8051907.313268.2.D5znj8"
sPattern = "(https:)*//((?!guang).)*\.taobao\.com/item\.htm.*$"
itemP = '^(https:)*//item\.taobao\.com/item\.htm.*$'
storeP = "^https://s\.taobao\.com/.*"
pages = set()
random.seed(datetime.datetime.now())

conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='root',db ='scrapy', use_unicode=True, charset="utf8")
cur = conn.cursor()

def crawl(surl, pattern, function):
    global pages   
    try:
        html = urllib2.urlopen(surl)
	page = html.read()
	soup = bs4.BeautifulSoup(page)
	#main_content = soup.find("div", {"class":"page-layout page-main-content"})
	#main_content = soup.find("",{"class":re.compile("^.*-main.*$")})
	#print ("main=%s" %(main_content.__str__()))
	urls = soup.findAll("a",href=re.compile(pattern))
	f = open('run.log','a')
	f.write(urls.__str__())
	f.close()
	#print ("urls=%s" %(urls))
	#function(urls)
        quene_url = []
        for url in urls:
            if 'href' in url.attrs:
		if url.attrs['href'] not in pages:
		    newPage = url.attrs['href']
		    pages.add(newPage)
                    kv = {}
   	            kv['url'] = newPage
		    if kv['url'].startswith("//"):
		        kv['url'] = "https:" + kv['url']
	                quene_url.append(kv)
		    #print ("kv=%s" %(kv))
	index_page(quene_url)
	print ("pages.size=%d" %(len(pages)))
    except:
	print ("crawl module has something wrong.")

def index_page(quene_url):
    print ("==============index=========")
    for kv in quene_url:
        if re.match(itemP, kv['url']):
	    print ("=========item========")
	    try:
		parse_item(kv['url'])
	    except AttributeError:
  		print ("item has error.")
	elif re.match(storeP, kv['url']):
	    print ("=========store===========")
	    print ("store url=%s" %(kv['url']))
	    crawl(kv[url], itemP, index_page)
	else:
	    print ("======crawl======")
	    print ("url=%s" %(kv['url']))
	    crawl(kv['url'], sPattern, index_page)	
	    
#    print ('counter=%s' %(urls.__len__()))
    

def parse_item(item_url):
    html = urllib2.urlopen(item_url)
    page = html.read()
    soup = bs4.BeautifulSoup(page)
    item = soup.find("",{"class":"tb-property tb-property-x"})
    title = item.find("",{"class":"tb-main-title"}).get_text()
    price = item.find("",{"class":"tb-rmb-num"}).get_text()
    store = soup.find(id="J_ShopInfo")
    s_name = store.find("",{"class":"tb-shop-name"}).dl.dd.strong.a.attrs['title']
    s_url = store.find("",{"class":"tb-shop-name"}).dl.dd.strong.a.attrs['href']
    print ("title=%s, price=%s, s_name=%s, s_url=%s" %(title, price, s_name, s_url))
    global cur
    global conn
    try:
        sql = "insert t_items(item_name,item_url,shop_name,shop_url) values(%s,%s,%s,%s)"
        cur.execute(sql, (title, item_url, s_name, s_url))
        conn.commit()
    except:
	print ("insert into mysql has error")
	traceback.print_exc()

    
if __name__ == "__main__":
    crawl(src_url, sPattern, index_page)
    cur.close()
    conn.close()


