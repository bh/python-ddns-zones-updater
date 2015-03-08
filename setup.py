import sys

from setuptools import setup

with open("README.rst") as readme_file:
    long_description = readme_file.read()

requirements = ['docopt', 'ipgetter', 'configobj']
if sys.version_info >= (3, 0):
    requirements += ["dnspython3"]
else:
    requirements += ["dnspython"]

if sys.version_info[:-3] == (2, 6):
    requirements += ['logutils']


setup(name="ddns-zones-updater",
      version="0.0.1dev",
      description=("DNSPython wrapper for manipulate DNS zones"
                   "configurations via dynamic updates (RFC 2136)"),
      long_description=long_description,
      author="Benjamin Hedrich",
      author_email="kiwisauce@pagenotfound.de",
      url="https://github.com/bh/python-ddns-zones-updater/",
      py_modules=('ddns_zones_updater',),
      include_package_data=True,
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              'ddns-zones-updater = ddns_zones_updater:main',
          ]
      })
