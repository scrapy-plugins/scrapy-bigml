from six.moves.urllib.parse import urlparse

from bigml.api import BigML

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
