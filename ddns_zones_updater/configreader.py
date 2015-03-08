from __future__ import absolute_import, unicode_literals

import logging

from configobj import ConfigObj

from .host import HostManager
from .key import KeyManager

log = logging.getLogger(__name__)


class InvalidConfig(Exception):
    pass


class ConfigReader(object):

    def __init__(self, config_path):
        log.info("Reading config file: %s" % config_path)
        self._config = ConfigObj(config_path)

        self.hosts = HostManager()
        self.keys = KeyManager()

    def _read_keys_from_config(self):
        for key_name, key_config in self._config['keys'].items():
            log.debug("Adding key '%s'" % key_name)
            self.keys.add(key_name, key_config['secret'])

    def _read_hosts_from_config(self):
        for title, host_config in self._config['hosts'].items():
            key_name = host_config['key']

            key = self.keys.get(key_name)
            if key is None:
                raise InvalidConfig("key with name %s does not exist!"
                                    % key_name)

            log.debug("Adding host '%s'" % title)
            self.hosts.add(name=host_config['name'], title=title, key=key,
                           zone=host_config['zone'],
                           dnsserver=host_config['dnsserver'])

    def read(self):
        self.interval = self._config['interval']
        self._read_keys_from_config()
        self._read_hosts_from_config()
