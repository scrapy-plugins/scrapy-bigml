============
scrapy-bigml
============

scrapy-bigml facilitates creating `BigML <https://bigml.com/>`_ sources and
datasets from `Scrapy <http://scrapy.org>`_ crawls. It can be used both as a
feed storage or as a pipeline.

BigML configuration
===================

Credentials
-----------

For both usage methods (feed storage or pipeline), you need to supply your
BigML credentials. You can do this either by supplying them as environment
variables::

    # in shell
    export BIGML_USERNAME=your_username
    export BIGML_API_KEY=your_apikey

Or by supplying them as Scrapy settings::

    BIGML_USERNAME = 'your_username'
    BIGML_API_KEY = 'your_api_key'

If you use scrapy-bigml as a feed storage, you can also provide them by adding
them to your feed URI::

    FEED_URI = 'bigml://your_username:your_api_key@your_source_name'

Development mode
----------------

During development, you probably want to enable BigML's dev mode::

    BIGML_DEVMODE = True

Usage as feed storage
=====================

scrapy-bigml can be used as storage backend on top of Scrapy's `feed exports
<http://doc.scrapy.org/en/stable/topics/feed-exports.html>`_. To use it, adjust
your Scrapy settings by setting the feed format to either ``csv`` (preferred)
or ``json``, enabling the ``bigml`` feed storage and providing a corresponding
feed URI with the name you wish to use for your BigML source::

    FEED_FORMAT = 'csv'
    FEED_STORAGES = {'bigml': 'scrapy_bigml.BigMLFeedStorage'}
    FEED_URI = 'bigml://your_source_name'

A spider with example configuration can be found in
``example_spider_feedstorage.py``.

Usage as pipeline
=================

If you wish to use scrapy-bigml as a pipeline, all you need to do is enable the
pipeline::

    ITEM_PIPELINES = {'scrapy_bigml.BigMLPipeline': 500}

You should also set a name for your BigML source (if not, scrapy-bigml will
default to "Scrapy")::

    BIGML_SOURCE_NAME = 'Your source name'

A spider with example configuration can be found in
``example_spider_pipeline.py``.
