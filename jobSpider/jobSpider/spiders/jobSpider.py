# -*- coding: utf-8 -*-

from ..items import Job
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import traceback

class JobSpider(CrawlSpider):
	name = "job"
	allowed_domains = ["jobs.51job.com", "search.51job.com"]
	start_urls = ["http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=070200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=06%2C07%2C08&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=03&cotype=99&degreefrom=99&jobterm=99&companysize=03%2C05%2C06%2C07%2C04&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9"]
	#start_urls = ["http://jobs.51job.com/nanjing/78989613.html?s=0"]
	rules = [Rule(LinkExtractor(allow=('jobs\.51job\.com/nanjing.*$',)), callback="parse_item", follow=True)]

	def parse(self, response):
		els = response.xpath("//div[@id='resultList']/div[@class='el']")
		print ("======================")
		print ("count=%s" %(len(els)))
		for d in els:
			#text = d.xpath("//p/span/a/text()")
			#print ("======%s" %(text))
			item = self.load_item(d)
			#yield request(item['url'])

	def load_item(self, d):
		item = Job()
		position = d.xpath("p/span/a/@title").extract()[0]
		item['position'] = position
		item['url'] = d.xpath("p/span/a/@href").extract()[0]
		item['company'] = d.xpath("span[@class='t2']/a/@title").extract()[0]
		item['address'] = d.xpath("span[@class='t3']/text()").extract()[0]
		item['salary'] = d.xpath("span[@class='t4']/text()").extract()[0]
		item['publish'] = d.xpath("span[@class='t5']/text()").extract()[0]
		print ("==========item===%s" %(item))
		return item

	def detail_item(self, d):
		item = Job()
		try:
			position = d.xpath("//div[@class='cn']/h1[@title]/text()").extract()[0]
			company = d.xpath("//div[@class='cn']/span/text()").extract()[0]
			sal = d.xpath("//div[@class='cn']/strong/text()").extract()[0]
			item['position'] = position
			item['company'] = company
			item['salary'] = sal
		except:
			print ("============sth worng=============")
			print 'parsing ', d.url 
			traceback.print_exc()	
		return item

