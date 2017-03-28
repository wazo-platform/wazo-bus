xivo-bus [![Build Status](https://travis-ci.org/wazo-pbx/xivo-bus.png?branch=master)](https://travis-ci.org/wazo-pbx/xivo-bus)
========

xivo-bus is a library used internally in Wazo to communicate with other components
of Wazo using RabbitMQ


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py27,py3
```


Building xivo-bus
-----------------

Use the following commands to build `xivo-bus` manually. The resulting packages will be in the
parent directory.

```sh
dch -i  # Increment the version in the changelog
dpkg-buildpackage -us -uc
```
