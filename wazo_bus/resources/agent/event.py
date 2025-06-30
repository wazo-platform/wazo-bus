# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import MultiUserEvent, TenantEvent
from ..common.types import UUIDStr


class AgentCreatedEvent(TenantEvent):
    """A new agent has been created"""

    service = 'confd'
    name = 'agent_created'
    routing_key_fmt = 'config.agent.created'

    def __init__(self, agent_id: int, tenant_uuid: UUIDStr):
        content = {
            'id': int(agent_id),
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid)


class AgentDeletedEvent(TenantEvent):
    """An agent has been deleted"""

    service = 'confd'
    name = 'agent_deleted'
    routing_key_fmt = 'config.agent.deleted'

    def __init__(self, agent_id: int, tenant_uuid: UUIDStr):
        content = {
            'id': int(agent_id),
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid)


class AgentEditedEvent(TenantEvent):
    """An agent has been edited"""

    service = 'confd'
    name = 'agent_edited'
    routing_key_fmt = 'config.agent.edited'

    def __init__(self, agent_id: int, tenant_uuid: UUIDStr):
        content = {
            'id': int(agent_id),
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid)


class AgentPausedEvent(MultiUserEvent):
    """An agent was paused"""

    service = 'agentd'
    name = 'agent_paused'
    routing_key_fmt = 'status.agent.pause'
    required_acl_fmt = 'events.statuses.agents'

    def __init__(
        self,
        agent_id: int,
        agent_number: str,
        queue: str,
        reason: str,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ):
        content = {
            'agent_id': agent_id,
            'agent_number': agent_number,
            'paused': True,
            'paused_reason': reason or '',
            'queue': queue,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuids)


class AgentUnpausedEvent(MultiUserEvent):
    """An agent was unpaused"""

    service = 'agentd'
    name = 'agent_unpaused'
    routing_key_fmt = 'status.agent.unpause'
    required_acl_fmt = 'events.statuses.agents'

    def __init__(
        self,
        agent_id: int,
        agent_number: str,
        queue: str,
        reason: str,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ):
        content = {
            'agent_id': agent_id,
            'agent_number': agent_number,
            'paused': False,
            'paused_reason': reason or '',
            'queue': queue,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuids)


class AgentStatusUpdatedEvent(MultiUserEvent):
    """An agent status has changed"""

    service = 'calld'
    name = 'agent_status_update'
    routing_key_fmt = 'status.agent'
    required_acl_fmt = 'events.statuses.agents'

    def __init__(
        self,
        agent_id: int,
        status: str,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ):
        content = {
            'agent_id': int(agent_id),
            'status': status,
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(content, tenant_uuid, user_uuids)
