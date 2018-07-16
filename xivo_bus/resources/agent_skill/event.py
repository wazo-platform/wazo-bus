# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class AgentSkillConfigEvent(object):

    def __init__(self, agent_id, skill_id):
        self.agent_id = agent_id
        self.skill_id = skill_id

    def marshal(self):
        return {
            'agent_id': self.agent_id,
            'skill_id': self.skill_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['agent_id'],
            msg['skill_id']
        )

    def __eq__(self, other):
        return (
            self.agent_id == other.agent_id
            and self.skill_id == other.skill_id
        )

    def __ne__(self, other):
        return not self == other


class AgentSkillAssociatedEvent(AgentSkillConfigEvent):
    name = 'agent_skill_associated'
    routing_key = 'config.agents.skills.updated'


class AgentSkillDissociatedEvent(AgentSkillConfigEvent):
    name = 'agent_skill_dissociated'
    routing_key = 'config.agents.skills.deleted'
