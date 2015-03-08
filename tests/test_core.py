from __future__ import absolute_import, unicode_literals

import mock
import pytest

from ddns_zones_updater.configreader import ConfigReader
from ddns_zones_updater.core import DDNSZoneUpdater


@pytest.fixture
def fake_config_reader_with_two_hosts():
    host_1 = mock.Mock(do_update=mock.Mock())
    host_2 = mock.Mock(do_update=mock.Mock())

    class FakeHostManager(mock.Mock):
        __iter__ = mock.Mock(return_value=(h for h in [host_1, host_2]))

    class FakeConfigReader(mock.Mock):
        hosts = FakeHostManager()

    return [host_1, host_2], FakeConfigReader()


@pytest.fixture
def updater_without_calling_init(request):
    patcher = mock.patch.object(DDNSZoneUpdater, "__init__", return_value=None)
    patcher.start()
    request.addfinalizer(patcher.stop)

    return DDNSZoneUpdater("path/to/config.ini")


@mock.patch.object(ConfigReader, "read")
@mock.patch.object(ConfigReader, "__init__", return_value=None)
def test_initializer(mock_init, mock_read):
    DDNSZoneUpdater("/tmp/foo.ini")
    mock_init.assert_called_once_with("/tmp/foo.ini")
    mock_read.assert_called_once_with()


def test_get_current_wan_ip(updater_without_calling_init):
    updater = updater_without_calling_init
    with mock.patch("ipgetter.myip", return_value="149.0.0.31") as mock_my_ip:
        assert updater.current_wan_ip() == "149.0.0.31"
        mock_my_ip.assert_called_once_with()


def test_run(updater_without_calling_init, fake_config_reader_with_two_hosts):
    updater = updater_without_calling_init
    hosts, updater.config = fake_config_reader_with_two_hosts

    with mock.patch("ipgetter.myip", return_value="1.1.1.1") as mock_my_ip:
        updater.run()

        for host in hosts:
            host.do_update.assert_called_once_with("1.1.1.1")

        mock_my_ip.assert_called_once_with()


@mock.patch("time.sleep")
def test_autoupdate(mock_sleep, updater_without_calling_init):
    updater = updater_without_calling_init
    updater.config = mock.Mock(interval="0.1")

    # Here it is impossible to throw a KeyboardInterrupt or
    # SystemExit exception, because pytest will catch these.
    class FakeException(Exception):
        pass

    with mock.patch.object(DDNSZoneUpdater, "run") as mock_run:
        mock_run.side_effect = [
            "ok", "ok", "ok", FakeException("foo is invalid")]
        updater.autoupdate()

        assert mock_run.call_count == 4

    assert mock_sleep.call_args_list == [
        mock.call(0.1), mock.call(0.1), mock.call(0.1), mock.call(0.1)
    ]
