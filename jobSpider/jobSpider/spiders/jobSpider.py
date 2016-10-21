# -*- coding: utf-8 -*-

from ..items import Job
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request  
from scrapy import log
import traceback

class JobSpider(CrawlSpider):
	name = "job"
	allowed_domains = ["jobs.51job.com", "search.51job.com"]
	start_urls = ["http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=06%2C07%2C08&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE&keywordtype=2&lang=c&stype=1&postchannel=0000&workyear=03&cotype=99&degreefrom=99&jobterm=99&companysize=03%2C05%2C06%2C07%2C04&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9&curr_page=1","http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=06%2C07%2C08&keyword=%E5%A4%A7%E6%9    5%B0%E6%8D%AE&keywordtype=2&lang=c&stype=1&postchannel=0000&workyear=03&cotype=99&degreefrom=99&jobterm=99&companysize=03%2C05%2C06%2C07%2C04&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confir    mdate=9&curr_page=2"]
	#start_urls = ["http://jobs.51job.com/nanjing/78989613.html?s=0"]
	#rules = [Rule(LinkExtractor(allow=('jobs\.51job\.com/nanjing.*$',)), callback="parse_item", follow=True)]
	flag = True
	
	def parse(self, response):
		els = response.xpath("//div[@id='resultList']/div[@class='el']")
		print ("======================")
		print ("count=%s" %(len(els)))
		for d in els:
			item = self.load_item(d)
			yield Request(item['url'], meta={'item':item}, callback=self.detail_item)

		#if self.flag:
		#	log.msg(self.get_pages(response), level=log.DEBUG)
		#	self.flag = False

	def load_item(self, d):
		item = Job()
		position = d.xpath("p/span/a/@title").extract()[0]
		item['position'] = position
		item['url'] = d.xpath("p/span/a/@href").extract()[0]
		item['company'] = d.xpath("span[@class='t2']/a/@title").extract()[0]
		item['address'] = d.xpath("span[@class='t3']/text()").extract()[0]
		item['salary'] = d.xpath("span[@class='t4']/text()").extract()[0]
		item['publish'] = d.xpath("span[@class='t5']/text()").extract()[0]
		#print ("==========item===%s" %(item))
		return item

	def detail_item(self, response):
		item = response.meta['item']
		d = response.xpath("//div[contains(@class,'bmsg') and contains(@class,'job_msg')]")
		try:
			item['duty'] = d.xpath("*").extract()[0]
		except:
			print ("============sth worng=============")
			traceback.print_exc()	
		#print ('url=%s, d=%s' %(response.url, d)) 
		#print ("*********detail=%s" %(item))
		return item

	def get_pages(self, response):
		total_page = response.xpath("//div[@class='p_in']/span[1]/text()").extract()[0].strip()[1:2]
		total_page = int(total_page)
		init_url = self.start_urls[0][:-1]
		print ("=========total_page=%s" %(total_page))
		for i in range(2,total_page + 1):
			nurl = init_url + str(i)
			log.msg("nurl=======" + nurl, level=log.DEBUG)
			self.start_urls.append(nurl)
		return total_page
		
