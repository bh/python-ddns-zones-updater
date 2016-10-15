from __future__ import absolute_import, print_function, unicode_literals

import datetime
import logging
import socket

import dns.message
import dns.query
import dns.rdatatype
import dns.resolver
import dns.tsigkeyring
import dns.update

log = logging.getLogger(__name__)


class Host(object):

    def __init__(self, name, key, dnsserver, zone, title):
        # TODO: rework names
        self.name = name
        self.key = key
        self.dnsserver = dnsserver
        self.zone = zone
        self.title = title

    def get_published_ip(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [socket.gethostbyname(self.dnsserver)]
        answers = resolver.query(self.title, dns.rdatatype.A)
        return answers[0].address

    def build_keyring(self):
        return dns.tsigkeyring.from_text({self.key.name: self.key.secret})

    def do_update(self, current_ip):
        if self.get_published_ip() == current_ip:
            log.info("No IP change for host %s, skipping update" % self.title)
            return

        log.info("Setting IP (A record) to %s for name %s" %
                 (current_ip, self.name))

        keyring = self.build_keyring()
        update = dns.update.Update(self.zone, keyring=keyring)
        update.replace(self.name, 3600, dns.rdatatype.A, current_ip)
        response = dns.query.tcp(update, self.dnsserver)

        # TODO: handle response
        response


class HostManager(object):

    def __init__(self):
        self.hosts = []

    def add(self, name, key, dnsserver, zone, title):
        host = Host(name=name, key=key, dnsserver=dnsserver,
                    zone=zone, title=title)
        self.hosts.append(host)

    def __iter__(self):
        return iter(self.hosts)
