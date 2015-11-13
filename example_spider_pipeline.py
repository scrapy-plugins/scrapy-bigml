import sys
import os
sys.path.insert(0, os.getcwd())

from scrapy import Spider


class BigMLTestSpider(Spider):

    name = "bigml_example_spider"

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_bigml.BigMLPipeline': 500},
        'BIGML_DEVMODE': True,
        'BIGML_SOURCE_NAME': 'The BigML Example Spider Source, yay!'
    }

    start_urls = ['http://scrapy.org']

    def parse(self, response):
        for i in range(10):
            yield {'fast_field': i, 'slow_field': i/3}
