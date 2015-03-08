from __future__ import absolute_import, unicode_literals

import logging

try:
    from logging.config import dictConfig
except ImportError:  # pragma: no cover
    # Python 2.6
    from logutils.dictconfig import dictConfig


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'NOTSET',
        'handlers': ['console'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
        },
    },
    'formatters': {
        'default': {
            'format': ('[%(levelname)-7s] %(asctime)s.%(msecs)d '
                       '%(filename)s:%(lineno)s %(message)s'),
            "datefmt": '%Y-%m-%d %H:%M:%S'
        }
    },
}


dictConfig(LOGGING_CONFIG)


def set_loglevel(level):  # pragma: no cover
    """
    Set the loglevel for all registered logging handlers.
    """

    for handler in logging._handlerList:
        handler = handler()
        handler.setLevel(level)
