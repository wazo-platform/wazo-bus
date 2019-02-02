# -*- coding: utf-8 -*-
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from unittest import TestCase

from hamcrest import assert_that
from hamcrest import equal_to

from ..calls import CallCollectdEvent


class TestCallCollectdEvent(TestCase):
    def test_plugin_instance_validation_when_empty(self):
        event = CallCollectdEvent('', '')

        assert_that(event.plugin_instance, equal_to('<unknown>.<unknown>'))

    def test_plugin_instance_validation_when_only_invalid_chars(self):
        event = CallCollectdEvent('_&!* <,(*&^ .%#@$#)&(^', 'ééé')

        assert_that(event.plugin_instance, equal_to('<unknown>.<unknown>'))

    def test_plugin_instance_validation_when_some_invalid_chars(self):
        event = CallCollectdEvent('abc-déf gh-ij', 'some-thìng')

        assert_that(event.plugin_instance, equal_to('abc-dfgh-ij.some-thng'))

    def test_plugin_instance_validation_when_no_invalid_chars(self):
        event = CallCollectdEvent('something', 'another')

        assert_that(event.plugin_instance, equal_to('something.another'))
