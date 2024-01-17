# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from unittest import TestCase

from hamcrest import assert_that, equal_to

from ..calls import _BaseCallCollectdEvent


class CollectdCallTest(_BaseCallCollectdEvent):
    name = 'collectd_test_event'
    routing_key_fmt = 'collectd.test'


class TestCallCollectdEvent(TestCase):
    def test_plugin_instance_validation_when_empty(self):
        event = CollectdCallTest('', '')
        assert_that(event.plugin_instance, equal_to('<unknown>.<unknown>'))

    def test_plugin_validation_when_no_instance(self):
        event = CollectdCallTest('', None)
        assert_that(event.plugin_instance, equal_to('<unknown>'))

    def test_plugin_instance_validation_when_only_invalid_chars(self):
        event = CollectdCallTest('_&!* <,(*&^ .%#@$#)&(^', 'ééé')
        assert_that(event.plugin_instance, equal_to('<unknown>.<unknown>'))

    def test_plugin_instance_validation_when_some_invalid_chars(self):
        event = CollectdCallTest('abc-déf gh-ij', 'some-thìng')
        assert_that(event.plugin_instance, equal_to('abc-dfgh-ij.some-thng'))

    def test_plugin_instance_validation_when_no_invalid_chars(self):
        event = CollectdCallTest('something', 'another')
        assert_that(event.plugin_instance, equal_to('something.another'))
