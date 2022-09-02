# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class UserAgentAssociatedEvent(UserEvent):
    name = 'user_agent_associated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.updated'

    def __init__(self, agent_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super(UserAgentAssociatedEvent, self).__init__(content, tenant_uuid, user_uuid)


class UserAgentDissociatedEvent(UserEvent):
    name = 'user_agent_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.deleted'

    def __init__(self, agent_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super(UserAgentDissociatedEvent, self).__init__(content, tenant_uuid, user_uuid)
