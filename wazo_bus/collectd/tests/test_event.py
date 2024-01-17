# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from hamcrest import assert_that, calling, is_, raises

from ..common import CollectdEvent


class NoNameCollectdEvent(CollectdEvent):
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoRoutingKeyCollectdEvent(CollectdEvent):
    name = 'collectd_no_routing_key'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoPluginCollectdEvent(CollectdEvent):
    name = 'collectd_no_plugin'
    routing_key_fmt = 'collectd.test'
    plugin = None
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoPluginInstanceCollectdEvent(CollectdEvent):
    name = 'collectd_no_plugin_instance'
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = None
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoTypeCollectdEvent(CollectdEvent):
    name = 'collectd_no_type'
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = None
    type_instance = 'type_instance'
    values = ('1',)


class NoTypeInstanceCollectdEvent(CollectdEvent):
    name = 'collectd_no_type_instance'
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = None
    values = ('1',)


class NoValuesCollectdEvent(CollectdEvent):
    name = 'collectd_no_values'
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'


class ValidCollectdEvent(CollectdEvent):
    name = 'collectd_valid'
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)
    time = 12345


class ValidWithTimeCollectdEvent(CollectdEvent):
    name = 'collectd_valid_with_time'
    routing_key_fmt = 'collectd.test'
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)
    time = 12345


class TestCollectdEvent(TestCase):
    def test_is_valid(self):
        assert_that(calling(NoNameCollectdEvent), raises(TypeError))
        assert_that(calling(NoRoutingKeyCollectdEvent), raises(TypeError))
        assert_that(NoPluginCollectdEvent().is_valid(), is_(False))
        assert_that(NoPluginInstanceCollectdEvent().is_valid(), is_(False))
        assert_that(NoTypeCollectdEvent().is_valid(), is_(False))
        assert_that(NoTypeInstanceCollectdEvent().is_valid(), is_(False))
        assert_that(NoValuesCollectdEvent().is_valid(), is_(False))
        assert_that(ValidCollectdEvent().is_valid(), is_(True))
        assert_that(ValidWithTimeCollectdEvent().is_valid(), is_(True))
