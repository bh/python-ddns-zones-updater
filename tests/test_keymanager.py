from __future__ import absolute_import, unicode_literals

from ddns_zones_updater.key import Key, KeyManager


def test_manager_add():
    manager = KeyManager()
    manager.add(name="name", secret="secret")

    assert len(manager.keys) == 1
    assert isinstance(manager.keys[0], Key)


def test_manager_get_known():
    manager = KeyManager()
    key = Key(name="name", secret="secret")
    manager.keys = [key]
    assert manager.get("name") == key


def test_manager_get_unknown():
    manager = KeyManager()
    key = Key(name="known", secret="secret")
    manager.keys = [key]
    assert manager.get("unknown") is None

    manager.keys = []
    assert manager.get("unknown") is None
