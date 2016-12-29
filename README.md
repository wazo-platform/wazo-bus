xivo-bus [![Build Status](https://travis-ci.org/wazo-pbx/xivo-bus.png?branch=master)](https://travis-ci.org/wazo-pbx/xivo-bus)
========

xivo-bus is a library used internally in Wazo to communicate with other components
of Wazo using RabbitMQ


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py27
```
