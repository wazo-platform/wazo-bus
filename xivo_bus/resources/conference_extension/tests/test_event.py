# -*- coding: utf-8 -*-
# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import ConferenceExtensionConfigEvent


class ConcreteConferenceExtensionConfigEvent(ConferenceExtensionConfigEvent):
    name = 'trunk_endpoint_event'


CONFERENCE_ID = 1
EXTENSION_ID = 2


class TestConferenceExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'conference_id': CONFERENCE_ID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteConferenceExtensionConfigEvent(CONFERENCE_ID, EXTENSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteConferenceExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('conference_id', CONFERENCE_ID),
            has_property('extension_id', EXTENSION_ID)))
