from __future__ import absolute_import, unicode_literals

import logging
import time

import ipgetter

from .configreader import ConfigReader

log = logging.getLogger(__name__)


class DDNSZoneUpdater(object):

    def __init__(self, config_path):
        self.config = ConfigReader(config_path)
        self.config.read()

    def current_wan_ip(self):
        current_ip = ipgetter.myip()
        log.info("Current WAN IP is %s" % current_ip)
        return current_ip

    def run(self):
        current_wan_ip = self.current_wan_ip()
        for host in self.config.hosts:
            log.info("Updating host %s" % host.title)
            host.do_update(current_wan_ip)
