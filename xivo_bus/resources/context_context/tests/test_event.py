# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import ContextContextsAssociatedEvent


CONTEXT_ID = '1234'
CONTEXT_IDS = [1, 3, 2, 4, 6]


class TestContextContextConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'context_id': CONTEXT_ID,
            'context_ids': CONTEXT_IDS,
        }

    def test_marshal(self):
        command = ContextContextsAssociatedEvent(CONTEXT_ID, CONTEXT_IDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ContextContextsAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('context_id', CONTEXT_ID),
            has_property('context_ids', CONTEXT_IDS)))
