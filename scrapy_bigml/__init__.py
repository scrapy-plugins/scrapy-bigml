from six.moves.urllib.parse import urlparse
from tempfile import TemporaryFile

from bigml.api import BigML

from scrapy.exceptions import NotConfigured
from scrapy.exporters import CsvItemExporter
from scrapy.extensions.feedexport import BlockingFeedStorage


class BigMLAPIMixIn(object):

    BIGML_AUTH_ERRMSG = ("{errtype:s} BigML credentials. Please supply "
                         "BIGML_USERNAME and BIGML_API_KEY as either Scrapy "
                         "settings or environment variables.")

    # XXX: This should get a method to read BigML configuration from settings

    def get_bigml_api(self, *args, **kwargs):
        try:
            self.bigml = BigML(*args, **kwargs)
        except AttributeError:
            raise NotConfigured(self.BIGML_AUTH_ERRMSG.format(
                errtype='Missing'))
        if not self.check_bigml_auth():
            raise NotConfigured(self.BIGML_AUTH_ERRMSG.format(
                errtype='Invalid'))

    def check_bigml_auth(self):
        return self.bigml.list_projects('limit=1')['code'] == 200

    def export_to_bigml(self, path, name, as_dataset=False):
        source = self.bigml.create_source(file, {'name': name})
        if not as_dataset:
            return source
        return self.bigml.create_dataset(source, {'name': name})


class BigMLFeedStorage(BlockingFeedStorage, BigMLAPIMixIn):

    def __init__(self, uri):
        # Parsing done in open() so we can access settings properly
        self.uri = uri

    def open(self, spider):
        # XXX: Hijacking this so we can access settings properly, see
        # https://github.com/scrapy/scrapy/issues/1567
        self.settings = spider.settings
        u = urlparse(self.uri)
        self.source_name = u.hostname or self.settings['BIGML_SOURCE_NAME']
        # TODO: May raise NotConfigured, but Scrapy can only handle it in
        #       __init__?
        self.get_bigml_api(
            username=u.username or self.settings['BIGML_USERNAME'],
            api_key=u.password or self.settings['BIGML_API_KEY'],
            dev_mode=self.settings.getbool('BIGML_DEVMODE', False)
        )
        return super(BigMLFeedStorage, self).open(spider)

    def _store_in_thread(self, file):
        file.seek(0)
        self.export_to_bigml(file, self.source_name)


class BigMLPipeline(BigMLAPIMixIn):

    AUTH_ERRMSG = ("{errtype:s} BigML credentials. Please supply BIGML_USERNAME"
                   " and BIGML_API_KEY as either Scrapy settings or environment"
                   " variables.")

    def __init__(self, username=None, api_key=None, source_name=None,
                 dev_mode=None):
        self.source_name = source_name
        self.get_bigml_api(username, api_key, dev_mode=dev_mode)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(
            username=crawler.settings['BIGML_USERNAME'],
            api_key=crawler.settings['BIGML_API_KEY'],
            source_name=crawler.settings.get('BIGML_SOURCE_NAME', 'Scrapy'),
            dev_mode=crawler.settings.getbool('BIGML_DEVMODE', False)
        )
        o.crawler = crawler
        o.settings = crawler.settings
        return o

    def open_spider(self, spider):
        self.tempfile = TemporaryFile(prefix='bigml-feed-')
        self.exporter = CsvItemExporter(self.tempfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.tempfile.seek(0)
        self.export_to_bigml(self.tempfile, self.source_name)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
