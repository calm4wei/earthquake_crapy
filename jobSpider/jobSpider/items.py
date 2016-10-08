# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	position = scrapy.Field()
	url = scrapy.Field()
	company = scrapy.Field()
	address = scrapy.Field()
	salary = scrapy.Field()
	publish = scrapy.Field()
	duty = scrapy.Field()
	#experience = scrapy.Field()
	#education = scrapy.Field()
	#publish = scrapy.Field
