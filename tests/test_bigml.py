import unittest

from scrapy.utils.spider import DefaultSpider
from scrapy.settings import Settings

from scrapy_bigml import BigMLFeedStorage


class BigMLFeedStorageTest(unittest.TestCase):

    def setup(self):
        self.projectname = "projectname"
        self.uri = "bigml://" + self.projectname

    def test_options_parsing(self):
        spider = DefaultSpider()
        spider.settings = Settings()
        spider.settings.setdict({
            'BIGML_USERNAME': 'sett_user',
            'BIGML_API_KEY': 'sett_apikey',
            'BIGML_SOURCE_NAME': 'sett_source'
        })

        storage = BigMLFeedStorage("bigml://")
        with storage.open(spider) as f:
            self.assertEqual(storage.username, 'sett_user')
            self.assertEqual(storage.api_key, 'sett_apikey')
            self.assertEqual(storage.source_name, 'sett_source')
            self.assertFalse(storage.dev_mode)

        spider.settings.set('BIGML_DEVMODE', True)
        storage = BigMLFeedStorage("bigml://user:apikey@source")
        with storage.open(spider) as f:
            self.assertEqual(storage.username, 'user')
            self.assertEqual(storage.api_key, 'apikey')
            self.assertEqual(storage.source_name, 'source')
            self.assertTrue(storage.dev_mode)
