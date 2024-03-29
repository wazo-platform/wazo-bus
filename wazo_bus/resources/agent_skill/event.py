# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class AgentSkillAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'agent_skill_associated'
    routing_key_fmt = 'config.agents.skills.updated'

    def __init__(
        self,
        agent_id: int,
        skill_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'agent_id': agent_id,
            'skill_id': skill_id,
        }
        super().__init__(content, tenant_uuid)


class AgentSkillDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'agent_skill_dissociated'
    routing_key_fmt = 'config.agents.skills.deleted'

    def __init__(
        self,
        agent_id: int,
        skill_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'agent_id': agent_id,
            'skill_id': skill_id,
        }
        super().__init__(content, tenant_uuid)
