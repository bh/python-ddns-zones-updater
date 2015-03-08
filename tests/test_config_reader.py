from __future__ import absolute_import, unicode_literals

import mock
import pytest

from ddns_zones_updater.configreader import ConfigReader, InvalidConfig
from ddns_zones_updater.host import HostManager
from ddns_zones_updater.key import Key, KeyManager


@mock.patch.object(KeyManager, "add")
def test_read_config_keys_extraction(mock_add, tmpdir):
    test_config = """\
    [keys]
        [[foo.bar.example.org]]
        secret = some_secret
    """
    test_file = tmpdir.join("foo.ini")
    test_file.write_text(test_config, encoding="utf-8")

    config_reader = ConfigReader(str(test_file))
    config_reader._read_keys_from_config()

    mock_add.assert_called_once_with('foo.bar.example.org', 'some_secret')


@mock.patch.object(HostManager, "add")
@mock.patch.object(KeyManager, "get")
def test_extract_hosts(mock_get, mock_add, tmpdir):

    test_config = """\
    [hosts]
        [[foo.bar.example.org]]
        name = foo
        zone = bar.example.org.
        dnsserver = example.org
        key = bla
    """
    test_file = tmpdir.join("foo.ini")
    test_file.write_text(test_config, encoding="utf-8")

    config_reader = ConfigReader(str(test_file))
    key_stub = Key('bla', 'secret')
    mock_get.return_value = key_stub

    config_reader._read_hosts_from_config()
    mock_add.assert_called_once_with(key=key_stub, title='foo.bar.example.org',
                                     name='foo', dnsserver='example.org',
                                     zone='bar.example.org.')


@mock.patch.object(KeyManager, "get")
def test_extract_hosts_invalid_unknown_key(mock_get, tmpdir):

    test_config = """\
    [hosts]
        [[foo.bar.example.org]]
        name = foo
        zone = bar.example.org.
        dnsserver = example.org
        key = blubb
    """
    test_file = tmpdir.join("foo.ini")
    test_file.write_text(test_config, encoding="utf-8")

    config_reader = ConfigReader(str(test_file))
    mock_get.return_value = None

    with pytest.raises(InvalidConfig) as bar:
        config_reader._read_hosts_from_config()

    assert bar.value.args[0] == 'key with name blubb does not exist!'


@mock.patch.object(ConfigReader, "_read_hosts_from_config")
@mock.patch.object(ConfigReader, "_read_keys_from_config")
def test_read(mock_read_keys_from_config, mock_read_hosts_from_config, tmpdir):
    test_config = """\
    interval = 3
    """
    test_file = tmpdir.join("foo.ini")
    test_file.write_text(test_config, encoding="utf-8")

    config_reader = ConfigReader(str(test_file))
    config_reader.read()

    mock_read_hosts_from_config.assert_called_once_with()
    mock_read_keys_from_config.assert_called_once_with()

    assert config_reader.interval == "3"
