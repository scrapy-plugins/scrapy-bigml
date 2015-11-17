import mock
import unittest

from scrapy.exceptions import NotConfigured
from scrapy.utils.spider import DefaultSpider
from scrapy.settings import Settings

from scrapy_bigml import BigMLAPIMixIn, BigMLFeedStorage, BigMLPipeline, BigML


class BigMLAPIMixInTest(unittest.TestCase):

    def setUp(self):
        self.bigml = BigMLAPIMixIn()

    @mock.patch.object(BigML, 'list_projects')
    def test_get_bigml_api_check_bigml_auth(self, mock_bigml_lp):
        # Uncomplete credentials
        with self.assertRaises(NotConfigured):
            self.bigml.get_bigml_api(username='username_only')
        with self.assertRaises(NotConfigured):
            self.bigml.get_bigml_api(api_key='api_key_only')
        # Wrong credentials
        mock_bigml_lp.return_value = {'code': 402}
        with self.assertRaises(NotConfigured):
            self.bigml.get_bigml_api(username='bad_user', api_key='bad_key')
        # Correct credentials
        mock_bigml_lp.return_value = {'code': 200}
        self.bigml.get_bigml_api(username='good_user', api_key='good_key')


class BigMLFeedStorageTest(unittest.TestCase):

    def test_options_parsing(self):
        spider = DefaultSpider()
        spider.settings = Settings()
        spider.settings.setdict({
            'BIGML_USERNAME': 'sett_user',
            'BIGML_API_KEY': 'sett_apikey',
            'BIGML_SOURCE_NAME': 'sett_source'
        })

        with mock.patch.object(BigMLFeedStorage, 'get_bigml_api') as m:
            storage = BigMLFeedStorage("bigml://")
            with storage.open(spider):
                m.assert_called_once_with(username='sett_user',
                                          api_key='sett_apikey',
                                          dev_mode=False)
                self.assertEqual(storage.source_name, 'sett_source')
                m.reset_mock()

            spider.settings.set('BIGML_DEVMODE', True)
            storage = BigMLFeedStorage("bigml://user:apikey@source")
            with storage.open(spider):
                m.assert_called_once_with(username='user', api_key='apikey',
                                          dev_mode=True)
                self.assertEqual(storage.source_name, 'source')


class BigMLPipelineTest(unittest.TestCase):

    # TODO
    pass
