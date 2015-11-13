============
scrapy-bigml
============

scrapy-bigml is a `Scrapy <http://scrapy.org>`_ pipeline that facilitates
creating `BigML <https://bigml.com/>`_ sources and datasets from Scrapy crawls.

Usage
=====

scrapy-bigml is implemented as a storage backend on top of Scrapy's `feed
exports <http://doc.scrapy.org/en/stable/topics/feed-exports.html>`_. To use
it, adjust your Scrapy settings by setting the feed format to either ``csv``
(preferred) or ``json``, enabling the ``bigml`` feed storage and providing a
corresponding feed URI with the name you wish to use for your BigML source::

    FEED_FORMAT = 'csv'
    FEED_STORAGES = {'bigml': 'scrapy_bigml.BigMLFeedStorage'}
    FEED_URI = 'bigml://your_source_name'

During development, you probably also want to enable BigML's dev mode::

    BIGML_DEVMODE = True

Additionally, you need to provide your BigML credentials. You can do this
either by supplying them as environment variables::

    # in shell
    export BIGML_USERNAME=your_username
    export BIGML_API_KEY=your_apikey

Or by supplying them as Scrapy settings::

    BIGML_USERNAME = 'your_username'
    BIGML_API_KEY = 'your_api_key'

Or by adding them to your feed URI::

    FEED_URI = 'bigml://your_username:your_api_key@your_source_name'

A spider with example configuration can be found in ``example_spider.py``.
