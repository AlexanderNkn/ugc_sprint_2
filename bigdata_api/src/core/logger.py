from core.logging_filters import RequestIdFilter


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'logstash': {
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'args': '("%(host)s", %(port)s, %(database_path)s, "%(transport)s", %(enable)s)',
            'transport': 'logstash_async.transport.UdpTransport',
            'host': 'logstash',
            'port': 5044,
            'enable': True,
            'database_path': None
        }
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access', 'logstash'],
            'level': 'INFO',
            'propagate': False,
        },
        'logstash': {
            'handlers': ['logstash'],
            'propagate': True,
        }
    },
    'filters': {
        'request_id': {
            '()': RequestIdFilter,
        }
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
