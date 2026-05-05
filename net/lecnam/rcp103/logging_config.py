import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'brief': {
            'format': '%(levelname)s: %(message)s'
        },
        'precise': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'filters': {
        'allow_foo': {
            '()': 'logging.Filter',
            'name': 'foo'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief',
            'level': 'DEBUG',
            'filters': ['allow_foo'],
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'precise',
            'filename': 'logconfig.log',
            'maxBytes': 1024,
            'backupCount': 3
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)