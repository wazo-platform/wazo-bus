# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
