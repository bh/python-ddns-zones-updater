Python DDNS zones updater
=========================
|Build Status| |Coveralls| |License| |Stars| |Requirements|

Description
-----------
DNSPython wrapper for manipulate DNS zones configurations via
dynamic updates (`RFC 2136 <https://www.ietf.org/rfc/rfc2136.txt>`_)

Installation
------------

on all other Unix/Linux systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Note: This Python package is not available at Cheeshop!

Use ``pip`` to install:

.. code:: bash

    $ pip install https://github.com/bh/python-ddns-zones-updater/archive/master.zip

on Arch Linux
^^^^^^^^^^^^^

TODO: Create an AUR package

Usage
-----

You can see the usage with:

.. code:: bash

    $ python-keepass-httpd --help

The output should be look like this:

::

    Usage:
      ddns-zones-updater [options]
      ddns-zones-updater (-h | --help)
      ddns-zones-updater --version

    Options:
      --help                    Show this screen
      -v --version              Show version
      -l --loglevel LOGLEVEL    Loglevel to use [default: INFO]
      -c --config=<path>        Config file to use [default: /etc/ddns-zones-updater.cfg]

A config file looks like:

.. code:: ini

    loglevel = INFO
    interval = 3600

    [keys]
        [[foo.bar.example.org]]
        secret = some_secret

    [hosts]
        [[foo.bar.example.org]]
        name = foo
        zone = bar.example.org.
        dnsserver = example.org
        key = foo.bar.example.org

Starting the service:
.. code:: bash

    $ ddns-zones-updater -c ~/config.ini

It prints something like when the IP is up to date:

::

    [INFO   ] 2015-03-08 16:32:04.718 configreader.py:20 Reading config file: /home/bh/foo.ini
    [DEBUG  ] 2015-03-08 16:32:04.718 configreader.py:28 Adding key 'oc.home.pagenotfound.de'
    [DEBUG  ] 2015-03-08 16:32:04.718 configreader.py:40 Adding host 'oc.home.pagenotfound.de'
    [INFO   ] 2015-03-08 16:32:07.869 core.py:21 Current WAN IP is 178.0.223.200
    [INFO   ] 2015-03-08 16:32:07.869 core.py:27 Updating host foo.bar.example.org
    [INFO   ] 2015-03-08 16:32:07.877 host.py:37 No IP change for host foo.bar.example.org, skipping update

The following when the IP is not up to date:

::

    [INFO   ] 2015-03-08 16:39:49.284 configreader.py:20 Reading config file: /home/bh/foo.ini
    [DEBUG  ] 2015-03-08 16:39:49.284 configreader.py:28 Adding key 'foo.bar.example.org'
    [DEBUG  ] 2015-03-08 16:39:49.284 configreader.py:40 Adding host 'foo.bar.example.org'
    [INFO   ] 2015-03-08 16:39:52.816 core.py:21 Current WAN IP is 178.0.223.200
    [INFO   ] 2015-03-08 16:39:52.816 core.py:27 Updating host foo.bar.example.org
    [INFO   ] 2015-03-08 16:39:52.824 host.py:41 Setting IP (A record) to 178.0.223.200 for name foo

Check
^^^^^

With nslookup:

.. code:: bash

    $ nslookup

    > server example.org
    Default server: example.org
    Address: 1.1.1.1#53
    > foo.bar.example.org
    Server:         example.org
    Address:        1.1.1.1#53

    Name:   foo.bar.example.org
    Address: 178.0.223.200

With dig:

.. code:: bash

    $ dig @example.org foo.bar.example.org

    [...]
    ;; QUESTION SECTION:
    ;foo.bar.example.org.       IN      A

    ;; ANSWER SECTION:
    foo.bar.example.org. 3600   IN      A       178.0.223.200
    [...]

Or the BIND zone config file on server:

.. code:: bash

    $ cat /etc/bind/zones/bar.example.org

    [...]
    $ORIGIN bar.example.org.
    $TTL 3600       ; 1 hour
    foo                      A       178.0.223.200
    [...]

.. |Build Status| image:: https://travis-ci.org/bh/python-ddns-zones-updater.svg?branch=master
    :target: https://travis-ci.org/bh/python-ddns-zones-updater
.. |Coveralls| image:: https://coveralls.io/repos/bh/python-ddns-zones-updater/badge.svg?branch=master 
    :target: https://coveralls.io/r/bh/python-ddns-zones-updater?branch=master
.. |License| image:: https://img.shields.io/badge/license-GPLv2-blue.svg   
    :target: https://raw.githubusercontent.com/bh/python-ddns-zones-updater/master/LICENSE
.. |Stars| image:: https://img.shields.io/github/stars/bh/python-ddns-zones-updater.svg   
    :target: https://github.com/bh/python-ddns-zones-updater/stargazers
.. |Requirements| image:: https://requires.io/github/bh/python-ddns-zones-updater/requirements.svg?branch=master
    :target: https://requires.io/github/bh/python-ddns-zones-updater/requirements/?branch=master
    :alt: Requirements Status


