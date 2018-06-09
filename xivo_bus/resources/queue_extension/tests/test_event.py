# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import QueueExtensionConfigEvent


class ConcreteQueueExtensionConfigEvent(QueueExtensionConfigEvent):
    name = 'queue_extension_associated'


QUEUE_ID = 1
EXTENSION_ID = 2


class TestQueueExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'queue_id': QUEUE_ID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteQueueExtensionConfigEvent(QUEUE_ID, EXTENSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteQueueExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('queue_id', QUEUE_ID),
            has_property('extension_id', EXTENSION_ID)
        ))
