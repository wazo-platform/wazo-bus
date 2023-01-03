# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent, UserEvent


class QueueMemberAgentAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_member_agent_associated'
    routing_key_fmt = 'config.queues.agents.updated'

    def __init__(self, queue_id, agent_id, penalty, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'agent_id': agent_id,
            'penalty': penalty,
        }
        super(QueueMemberAgentAssociatedEvent, self).__init__(content, tenant_uuid)


class QueueMemberAgentDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_member_agent_dissociated'
    routing_key_fmt = 'config.queues.agents.deleted'

    def __init__(self, queue_id, agent_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'agent_id': agent_id,
        }
        super(QueueMemberAgentDissociatedEvent, self).__init__(content, tenant_uuid)


class QueueMemberUserAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'queue_member_user_associated'
    routing_key_fmt = 'config.queues.users.updated'

    def __init__(self, queue_id, tenant_uuid, user_uuid):
        content = {
            'queue_id': queue_id,
            'user_uuid': str(user_uuid),
        }
        super(QueueMemberUserAssociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class QueueMemberUserDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'queue_member_user_dissociated'
    routing_key_fmt = 'config.queues.users.deleted'

    def __init__(self, queue_id, tenant_uuid, user_uuid):
        content = {
            'queue_id': queue_id,
            'user_uuid': str(user_uuid),
        }
        super(QueueMemberUserDissociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
