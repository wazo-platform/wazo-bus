xivo-bus [![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=xivo-bus)](https://jenkins.wazo.community/job/xivo-bus)
========

xivo-bus is a library used internally in Wazo to communicate with other components
of Wazo using RabbitMQ


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py37
```

Running integration tests
-------------------------

```sh
tox -e integration
```


Building xivo-bus
-----------------

Use the following commands to build `xivo-bus` manually. The resulting packages will be in the
parent directory.

```sh
dch -i  # Increment the version in the changelog
dpkg-buildpackage -us -uc
```
