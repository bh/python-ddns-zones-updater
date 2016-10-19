from __future__ import absolute_import, unicode_literals

import dns.rdatatype
import dns.resolver
import mock
import pytest

from ddns_zones_updater.host import Host
from ddns_zones_updater.key import Key


class FakeUpdate(mock.Mock):
    replace = mock.Mock()
    add = mock.Mock()


@pytest.fixture
def fake_host():
    key = Key(name="keyname", secret="secret")
    host = Host(name="name", title="title", key=key,
                zone="zone",
                dnsserver="dnsserver")
    return host


def test_build_keyring(fake_host):

    with mock.patch("dns.tsigkeyring.from_text") as mock_from_text:
        fake_host.build_keyring()
        mock_from_text.assert_called_once_with({'keyname': 'secret'})


@mock.patch("socket.gethostbyname")
@mock.patch.object(dns.resolver.Resolver, "query")
def test_published_ip(mock_query, mock_gethostbyname, fake_host):
    fake_host.title = "bla.foo.org"
    fake_host.dnsserver = "foo.org"
    mock_gethostbyname.return_value = "8.8.8.8"
    fake_host.get_published_ip()
    mock_query.assert_called_once_with("bla.foo.org", dns.rdatatype.A)


@mock.patch("dns.update.Update", FakeUpdate)
@mock.patch.object(FakeUpdate, "__init__", return_value=None)
@mock.patch.object(FakeUpdate, "replace")
@mock.patch.object(Host, "build_keyring", return_value={"keyname": "secret"})
@mock.patch.object(Host, "get_published_ip")
@mock.patch("dns.query.tcp", return_value=None)
def test_do_update_for_host_changed_ip(mock_tcp, mock_get_published_ip,
                                       mock_build_keyring, mock_replace,
                                       mock_update, fake_host):

    mock_get_published_ip.return_value = "149.0.0.30"
    fake_host.do_update(current_ip="10.1.1.1")

    mock_replace.assert_called_once_with(
        'name', 3600, dns.rdatatype.A, '10.1.1.1')
    mock_update.assert_called_once_with('zone', keyring={'keyname': 'secret'})
    mock_tcp.assert_called_once_with(mock.ANY, "dnsserver")


@mock.patch("dns.update.Update", FakeUpdate)
@mock.patch.object(FakeUpdate, "__init__", return_value=None)
@mock.patch.object(FakeUpdate, "replace")
@mock.patch.object(Host, "build_keyring", return_value={"keyname": "secret"})
@mock.patch.object(Host, "get_published_ip")
@mock.patch("dns.query.tcp", return_value=None)
def test_do_update_for_host_not_changed(mock_tcp, mock_get_published_ip,
                                        mock_build_keyring, mock_replace,
                                        mock_update, fake_host):

    mock_get_published_ip.return_value = "10.1.1.1"
    fake_host.do_update(current_ip="10.1.1.1")

    assert not mock_replace.called
    assert not mock_tcp.called

@mock.patch("dns.update.Update", FakeUpdate)
@mock.patch.object(FakeUpdate, "__init__", return_value=None)
@mock.patch.object(FakeUpdate, "add")
@mock.patch.object(Host, "build_keyring", return_value={"keyname": "secret"})
@mock.patch.object(Host, "get_published_ip")
@mock.patch("dns.query.tcp", return_value=None)
def test_do_force_update_for_host(mock_tcp, mock_get_published_ip,
                                  mock_build_keyring, mock_add,
                                  mock_update, fake_host):

    mock_get_published_ip.side_effect = dns.resolver.NXDOMAIN()
    fake_host.do_update(current_ip="10.1.1.1")

    assert mock_add.called
    assert mock_tcp.called
