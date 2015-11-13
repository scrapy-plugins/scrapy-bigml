from six.moves.urllib.parse import urlparse
from tempfile import TemporaryFile

from bigml.api import BigML

from scrapy.exceptions import NotConfigured
from scrapy.exporters import CsvItemExporter
from scrapy.extensions.feedexport import BlockingFeedStorage


class BigMLFeedStorage(BlockingFeedStorage):

    def __init__(self, uri):
        # Parsing done in open() so we can access settings properly
        self.uri = uri

    def open(self, spider):
        # XXX: Hijacking this so we can access settings properly, see
        # https://github.com/scrapy/scrapy/issues/1567
        self.settings = spider.settings
        u = urlparse(self.uri)
        self.username = u.username or self.settings['BIGML_USERNAME']
        self.api_key = u.password or self.settings['BIGML_API_KEY']
        self.source_name = u.hostname or self.settings['BIGML_SOURCE_NAME']
        self.dev_mode = self.settings.getbool('BIGML_DEVMODE', False)
        return super(BigMLFeedStorage, self).open(spider)

    def _store_in_thread(self, file):
        file.seek(0)
        api = BigML(self.username, self.api_key, dev_mode=self.dev_mode)
        api.create_source(file, {'name': self.source_name})


class BigMLPipeline(object):

    AUTH_ERRMSG = ("{errtype:s} BigML credentials. Please supply BIGML_USERNAME"
                   " and BIGML_API_KEY as either Scrapy settings or environment"
                   " variables.")

    def __init__(self, username=None, api_key=None, source_name=None,
                 dev_mode=None):
        self.username = username
        self.api_key = api_key
        self.source_name = source_name
        self.dev_mode = dev_mode
        self.api = self._get_api()

    @classmethod
    def from_crawler(cls, crawler):
        pl = cls(
            username=crawler.settings['BIGML_USERNAME'],
            api_key=crawler.settings['BIGML_API_KEY'],
            source_name=crawler.settings.get('BIGML_SOURCE_NAME', 'Scrapy'),
            dev_mode=crawler.settings.getbool('BIGML_DEVMODE', False)
        )
        pl.crawler = crawler
        pl.settings = crawler.settings
        return pl

    def _get_api(self):
        try:
            api = BigML(self.username, self.api_key, dev_mode=self.dev_mode)
        except AttributeError:
            raise NotConfigured(self.AUTH_ERRMSG.format(errtype='Missing'))
        if api.list_projects('limit=1')['code'] != 200:
            raise NotConfigured(self.AUTH_ERRMSG.format(errtype='Invalid'))
        return api

    def open_spider(self, spider):
        self.tempfile = TemporaryFile(prefix='bigml-feed-')
        self.exporter = CsvItemExporter(self.tempfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.tempfile.seek(0)
        self.api.create_source(self.tempfile, {'name': self.source_name})

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
