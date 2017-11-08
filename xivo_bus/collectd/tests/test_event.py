# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from unittest import TestCase

from hamcrest import assert_that, is_

from ..common import CollectdEvent


class NoPluginCollectdEvent(CollectdEvent):
    plugin = None
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoPluginInstanceCollectdEvent(CollectdEvent):
    plugin = 'plugin'
    plugin_instance = None
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)


class NoTypeCollectdEvent(CollectdEvent):
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = None
    type_instance = 'type_instance'
    values = ('1',)


class NoTypeInstanceCollectdEvent(CollectdEvent):
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = None
    values = ('1',)


class NoValuesCollectdEvent(CollectdEvent):
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'


class ValidCollectdEvent(CollectdEvent):
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)
    time = 12345


class ValidWithTimeCollectdEvent(CollectdEvent):
    plugin = 'plugin'
    plugin_instance = 'plugin_instance'
    type_ = 'type'
    type_instance = 'type_instance'
    values = ('1',)
    time = 12345


class TestCollectdEvent(TestCase):
    def test_is_valid(self):
        assert_that(CollectdEvent().is_valid(), is_(False))
        assert_that(NoPluginCollectdEvent().is_valid(), is_(False))
        assert_that(NoPluginInstanceCollectdEvent().is_valid(), is_(False))
        assert_that(NoTypeCollectdEvent().is_valid(), is_(False))
        assert_that(NoTypeInstanceCollectdEvent().is_valid(), is_(False))
        assert_that(NoValuesCollectdEvent().is_valid(), is_(False))

        assert_that(ValidCollectdEvent().is_valid(), is_(True))
        assert_that(ValidWithTimeCollectdEvent().is_valid(), is_(True))
