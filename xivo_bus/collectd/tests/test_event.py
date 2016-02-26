# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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

from hamcrest import assert_that, is_
from unittest import TestCase

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
