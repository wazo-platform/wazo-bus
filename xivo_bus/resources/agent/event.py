# -*- coding: utf-8 -*-
# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, BaseEvent, ResourceConfigEvent


class AgentCreatedEvent(TenantEvent):
    name = 'agent_created'
    routing_key_fmt = 'config.agent.created'

    def __init__(self, agent_id, tenant_uuid):
        content = {'id': int(agent_id)}
        super(AgentCreatedEvent, self).__init__(content, tenant_uuid)


class AgentDeletedEvent(TenantEvent):
    name = 'agent_deleted'
    routing_key_fmt = 'config.agent.deleted'

    def __init__(self, agent_id, tenant_uuid):
        content = {'id': int(agent_id)}
        super(AgentDeletedEvent, self).__init__(content, tenant_uuid)


class AgentEditedEvent(TenantEvent):
    name = 'agent_edited'
    routing_key_fmt = 'config.agent.edited'

    def __init__(self, agent_id, tenant_uuid):
        content = {'id': int(agent_id)}
        super(AgentEditedEvent, self).__init__(content, tenant_uuid)


class PauseAgentEvent(BaseEvent):
    name = 'agent_paused'
    routing_key = 'status.agent.pause'
    required_acl = 'events.statuses.agents'

    def __init__(self, agent_id, agent_number, queue, reason=''):
        self._body = dict(
            agent_id=agent_id,
            agent_number=agent_number,
            paused=True,
            paused_reason=reason,
            queue=queue,
        )


class UnpauseAgentEvent(BaseEvent):
    name = 'agent_unpaused'
    routing_key = 'status.agent.unpause'
    required_acl = 'events.statuses.agents'

    def __init__(self, agent_id, agent_number, queue, reason=''):
        self._body = dict(
            agent_id=agent_id,
            agent_number=agent_number,
            paused=False,
            paused_reason=reason,
            queue=queue,
        )


# To be removed, needed for migration
class EditAgentEvent(ResourceConfigEvent):
    name = 'agent_edited'
    routing_key = 'config.agent.edited'


# To be removed, needed for migration
class DeleteAgentEvent(ResourceConfigEvent):
    name = 'agent_deleted'
    routing_key = 'config.agent.deleted'
