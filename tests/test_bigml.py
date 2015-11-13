import mock
import unittest

from scrapy.exceptions import NotConfigured
from scrapy.utils.spider import DefaultSpider
from scrapy.settings import Settings

from scrapy_bigml import BigMLFeedStorage, BigMLPipeline, BigML


class BigMLFeedStorageTest(unittest.TestCase):

    def test_options_parsing(self):
        spider = DefaultSpider()
        spider.settings = Settings()
        spider.settings.setdict({
            'BIGML_USERNAME': 'sett_user',
            'BIGML_API_KEY': 'sett_apikey',
            'BIGML_SOURCE_NAME': 'sett_source'
        })

        storage = BigMLFeedStorage("bigml://")
        with storage.open(spider):
            self.assertEqual(storage.username, 'sett_user')
            self.assertEqual(storage.api_key, 'sett_apikey')
            self.assertEqual(storage.source_name, 'sett_source')
            self.assertFalse(storage.dev_mode)

        spider.settings.set('BIGML_DEVMODE', True)
        storage = BigMLFeedStorage("bigml://user:apikey@source")
        with storage.open(spider):
            self.assertEqual(storage.username, 'user')
            self.assertEqual(storage.api_key, 'apikey')
            self.assertEqual(storage.source_name, 'source')
            self.assertTrue(storage.dev_mode)


class BigMLPipelineTest(unittest.TestCase):

    @mock.patch.object(BigML, 'list_projects')
    def test_get_api(self, mock_bigml_lp):
        # Uncomplete credentials
        with self.assertRaises(NotConfigured):
            BigMLPipeline(username='username_only')
        with self.assertRaises(NotConfigured):
            BigMLPipeline(api_key='api_key_only')
        # Wrong credentials
        mock_bigml_lp.return_value = {'code': 402}
        with self.assertRaises(NotConfigured):
            BigMLPipeline(username='bad_user', api_key='bad_api_key')
        # Correct credentials
        mock_bigml_lp.return_value = {'code': 200}
        BigMLPipeline(username='good_user', api_key='good_api_key')
