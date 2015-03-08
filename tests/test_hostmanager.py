from __future__ import absolute_import, unicode_literals

from ddns_zones_updater.host import Host, HostManager


def test_manager_add():
    manager = HostManager()
    manager.add(name="name", title="title", key="key",
                zone="zone",
                dnsserver="dnsserver")

    assert len(manager.hosts) == 1
    assert isinstance(manager.hosts[0], Host)


def test_manager_iter():
    manager = HostManager()
    manager.hosts = ["h1", "h2"]
    assert list(manager) == ["h1", "h2"]
