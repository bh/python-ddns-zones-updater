"""\
Usage:
  ddns-zones-updater [options]
  ddns-zones-updater (-h | --help)
  ddns-zones-updater --version

Options:
  --help                    Show this screen
  -v --version              Show version
  -l --loglevel LOGLEVEL    Loglevel to use [default: INFO]
  -c --config=<path>        Config file to use [default: /etc/ddns-zones-updater.cfg]
"""  # flake8: noqa
from __future__ import print_function, absolute_import

from . import log
import logging


import docopt


def main():
    arguments = docopt.docopt(__doc__)
    config_path = arguments["--config"]
    loglevel = arguments["--loglevel"]

    if loglevel is None:
        loglevel = logging.INFO

    log.set_loglevel(loglevel)

    logger = logging.getLogger(__name__)
    # import this here because of the logging configuration
    from .core import DDNSZoneUpdater
    updater = DDNSZoneUpdater(config_path=config_path)
    updater.run()
