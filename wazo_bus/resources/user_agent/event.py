# Copyright 2016-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import MultiUserEvent, UserEvent
from ..common.types import UUIDStr


class UserAgentAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_agent_associated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.updated'

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserAgentDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_agent_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.deleted'

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserAgentQueueSubscribedEvent(MultiUserEvent):
    service = 'agentd'
    name = 'user_agent_queue_subscribed'
    routing_key_fmt = 'agentd.agents.{agent_id}.queues.{queue_id}.subscribed'

    def __init__(
        self,
        agent_id: int,
        queue_id: int,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ):
        content = {
            'agent_id': agent_id,
            'queue_id': queue_id,
        }
        super().__init__(content, tenant_uuid, user_uuids)


class UserAgentQueueUnsubscribedEvent(MultiUserEvent):
    service = 'agentd'
    name = 'user_agent_queue_unsubscribed'
    routing_key_fmt = 'agentd.agents.{agent_id}.queues.{queue_id}.unsubscribed'

    def __init__(
        self,
        agent_id: int,
        queue_id: int,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ):
        content = {
            'agent_id': agent_id,
            'queue_id': queue_id,
        }
        super().__init__(content, tenant_uuid, user_uuids)
