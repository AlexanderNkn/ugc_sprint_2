import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'bigdata')

KAFKA_HOST = os.getenv('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = int(os.getenv('KAFKA_PORT', 9092))
KAFKA_INSTANCE = [f'{KAFKA_HOST}:{KAFKA_PORT}']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTH_HOST = os.getenv('AUTH_HOST', 'http://127.0.0.1')
AUTH_PORT = int(os.getenv('AUTH_PORT', 80))
AUTH_BASE_URL = os.getenv('AUTH_BASE_URL', '/auth-api/v1')
ENABLE_AUTHORIZATION = int(os.getenv('ENABLE_AUTHORIZATION', 0))

BIGDATASPI_PORT = int(os.getenv('BIGDATASPI_PORT', 8001))

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', 'http://127.0.0.1')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT', 5044))

SENTRY_DSN = os.getenv('SENTRY_DSN', '')
