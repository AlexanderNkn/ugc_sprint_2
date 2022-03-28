import logging

from logstash_async.handler import AsynchronousLogstashHandler

from core import config


def setup_logstash():
    host = config.LOGSTASH_HOST
    port = config.LOGSTASH_PORT
    logger = logging.getLogger('python-logstash-logger')
    logger.setLevel(logging.DEBUG)
    async_handler = AsynchronousLogstashHandler(host, port, database_path=None)
    logger.addHandler(async_handler)
