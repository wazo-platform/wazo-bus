# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to

from ..event import (
    CreateSoundEvent,
    DeleteSoundEvent,
)

SOUND_NAME = 'sound'


class TestSoundEvent(unittest.TestCase):

    def test_create_routing_key_fmt(self):
        msg = CreateSoundEvent(SOUND_NAME)
        assert_that(
            msg.routing_key,
            equal_to('config.sounds.created')
        )

    def test_delete_routing_key_fmt(self):
        msg = DeleteSoundEvent(SOUND_NAME)
        assert_that(
            msg.routing_key,
            equal_to('config.sounds.deleted')
        )
