# -*- coding: utf-8 -*-
# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest

from uuid import uuid4
from hamcrest import assert_that, equal_to

from ..event import GroupExtensionConfigEvent


class ConcreteGroupExtensionConfigEvent(GroupExtensionConfigEvent):
    name = 'group_extension_event'
    routing_key_fmt = 'config.groups.extensions.updated'


GROUP_ID = 1
GROUP_UUID = str(uuid4())
EXTENSION_ID = 2


class TestGroupExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'group_uuid': GROUP_UUID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteGroupExtensionConfigEvent(**self.msg)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteGroupExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event._body, equal_to(self.msg))
