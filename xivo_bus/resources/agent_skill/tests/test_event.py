# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_properties

from ..event import AgentSkillConfigEvent


class ConcreteAgentSkillConfigEvent(AgentSkillConfigEvent):
    name = 'agent_skill_event'


AGENT_ID = 1
SKILL_ID = 2


class TestAgentSkillConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'agent_id': AGENT_ID,
            'skill_id': SKILL_ID,
        }

    def test_marshal(self):
        command = ConcreteAgentSkillConfigEvent(AGENT_ID, SKILL_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteAgentSkillConfigEvent.unmarshal(self.msg)

        assert_that(event, has_properties(
            agent_id=AGENT_ID,
            skill_id=SKILL_ID,
        ))
