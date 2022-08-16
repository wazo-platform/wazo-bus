# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class AgentSkillAssociatedEvent(TenantEvent):
    name = 'agent_skill_associated'
    routing_key_fmt = 'config.agents.skills.updated'

    def __init__(self, agent_id, skill_id, tenant_uuid):
        content = {
            'agent_id': agent_id,
            'skill_id': skill_id,
        }
        super(AgentSkillAssociatedEvent, self).__init__(content, tenant_uuid)


class AgentSkillDissociatedEvent(TenantEvent):
    name = 'agent_skill_dissociated'
    routing_key_fmt = 'config.agents.skills.deleted'

    def __init__(self, agent_id, skill_id, tenant_uuid):
        content = {
            'agent_id': agent_id,
            'skill_id': skill_id,
        }
        super(AgentSkillDissociatedEvent, self).__init__(content, tenant_uuid)
