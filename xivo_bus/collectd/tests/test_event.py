# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from hamcrest import assert_that, is_, calling, raises

from ..common import AbstractCollectdEvent


class NoRoutingKeyCollectdEvent(AbstractCollectdEvent):
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoPluginCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = None
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoPluginInstanceCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = None
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoTypeCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = None
    type_instance = 'type_instance'
    values = ('1',)


class NoTypeInstanceCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = None
    values = ('1',)


class NoValuesCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'


class ValidCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)
    time = 12345


class ValidWithTimeCollectdEvent(AbstractCollectdEvent):
    routing_key = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)
    time = 12345


class TestCollectdEvent(TestCase):
    def test_is_valid(self):
        assert_that(calling(NoRoutingKeyCollectdEvent), raises(TypeError))
        assert_that(NoPluginCollectdEvent().is_valid(), is_(False))
        assert_that(NoPluginInstanceCollectdEvent().is_valid(), is_(False))
        assert_that(NoTypeCollectdEvent().is_valid(), is_(False))
        assert_that(NoTypeInstanceCollectdEvent().is_valid(), is_(False))
        assert_that(NoValuesCollectdEvent().is_valid(), is_(False))
        assert_that(ValidCollectdEvent().is_valid(), is_(True))
        assert_that(ValidWithTimeCollectdEvent().is_valid(), is_(True))
