# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditAgentEvent(ResourceConfigEvent):
    name = 'agent_edited'
    routing_key = 'config.agent.edited'


class CreateAgentEvent(ResourceConfigEvent):
    name = 'agent_created'
    routing_key = 'config.agent.created'


class DeleteAgentEvent(ResourceConfigEvent):
    name = 'agent_deleted'
    routing_key = 'config.agent.deleted'
