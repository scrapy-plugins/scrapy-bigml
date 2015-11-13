import sys
import os
sys.path.insert(0, os.getcwd())

from scrapy import Spider


class BigMLTestSpider(Spider):

    name = "bigml_example_spider"

    custom_settings = {
        'FEED_STORAGES': {'bigml': 'scrapy_bigml.BigMLFeedStorage'},
        'FEED_URI': 'bigml://scrapy',
        'FEED_FORMAT': 'csv',
        'BIGML_DEVMODE': True,
    }

    start_urls = ['http://scrapy.org']

    def parse(self, response):
        for i in range(10):
            yield {'fast_field': i, 'slow_field': i/3}
