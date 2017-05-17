# -*- coding: utf-8 -*-

# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
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

from unittest import TestCase
from uuid import uuid4
from hamcrest import assert_that, equal_to
from ..events import PluginInstallProgressEvent, PluginUninstallProgressEvent


def new_uuid():
    return str(uuid4())


class TestPluginInstallProgressEvent(TestCase):

    def test_marshal(self):
        uuid_ = new_uuid()
        status = 'start'

        event = PluginInstallProgressEvent(uuid_, status)

        result = event.marshal()
        expected = {'uuid': uuid_, 'status': status}

        assert_that(result, equal_to(expected))

    def test_unmarshal(self):
        uuid_ = new_uuid()
        status = 'building'

        body = {'uuid': uuid_, 'status': status}
        event = PluginInstallProgressEvent.unmarshal(body)
        expected = PluginInstallProgressEvent(uuid_, status)

        assert_that(event, equal_to(expected))


class TestPluginUninstallProgressEvent(TestCase):

    def test_marshal(self):
        uuid_ = new_uuid()
        status = 'start'

        event = PluginUninstallProgressEvent(uuid_, status)

        result = event.marshal()
        expected = {'uuid': uuid_, 'status': status}

        assert_that(result, equal_to(expected))

    def test_unmarshal(self):
        uuid_ = new_uuid()
        status = 'deleting'

        body = {'uuid': uuid_, 'status': status}
        event = PluginInstallProgressEvent.unmarshal(body)
        expected = PluginUninstallProgressEvent(uuid_, status)

        assert_that(event, equal_to(expected))
