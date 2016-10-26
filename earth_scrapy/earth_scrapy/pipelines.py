# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from elasticsearch import Elasticsearch

class EarthScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class EsPipeline(object):
	def __init__(self, es_uri, es_index, es_type):
		self.es = Elasticsearch(es_uri)
		self.es_index = es_index
		self.es_type = es_type

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			es_uri=crawler.settings.get('ES_URI'),
			es_index=crawler.settings.get('ES_INDEX'),
			es_type=crawler.settings.get('ES_TYPE')
		)
				
	def process_item(self, item, spider):
		obj = json.dumps(dict(item))
		self.es.index(index=self.es_index, doc_type=self.es_type, body=obj)
		return item

