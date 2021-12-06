# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent, BaseEvent


class EditAgentEvent(ResourceConfigEvent):
    name = 'agent_edited'
    routing_key = 'config.agent.edited'


class CreateAgentEvent(ResourceConfigEvent):
    name = 'agent_created'
    routing_key = 'config.agent.created'


class DeleteAgentEvent(ResourceConfigEvent):
    name = 'agent_deleted'
    routing_key = 'config.agent.deleted'


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
        self.agent_id = agent_id


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
        self.agent_id = agent_id
