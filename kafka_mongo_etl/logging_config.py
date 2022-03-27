LOGGING_CONFIG = {
    "version": 1,
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    },
    "loggers": {
        "etl_kafka_mongo": {},
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "INFO",
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
}
