from __future__ import absolute_import, unicode_literals


class Key(object):

    def __init__(self, name, secret):
        self.name = name
        self.secret = secret


class KeyManager(object):

    def __init__(self):
        self.keys = []

    def add(self, name, secret):
        self.keys.append(Key(name, secret))

    def get(self, name):
        try:
            return next(key for key in self.keys if key.name == name)
        except StopIteration:
            return None
