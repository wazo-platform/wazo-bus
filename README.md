wazo-bus [![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-bus)](https://jenkins.wazo.community/job/wazo-bus)
========

wazo-bus is a library used internally in Wazo to communicate with other components
of Wazo using RabbitMQ


Running unit tests
------------------

```
pip install tox
tox -e py39
```

Running integration tests
-------------------------

```sh
tox -e integration
```


Building wazo-bus
-----------------

Use the following commands to build `wazo-bus` manually. The resulting packages will be in the
parent directory.

```sh
dch -i  # Increment the version in the changelog
dpkg-buildpackage -us -uc
```
