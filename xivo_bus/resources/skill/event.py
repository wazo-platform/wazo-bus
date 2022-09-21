# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class SkillCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_created'
    routing_key_fmt = 'config.agents.skills.created'

    def __init__(self, skill_id, tenant_uuid):
        content = {'id': int(skill_id)}
        super(SkillCreatedEvent, self).__init__(content, tenant_uuid)


class SkillDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_deleted'
    routing_key_fmt = 'config.agents.skills.deleted'

    def __init__(self, skill_id, tenant_uuid):
        content = {'id': int(skill_id)}
        super(SkillDeletedEvent, self).__init__(content, tenant_uuid)


class SkillEditedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_edited'
    routing_key_fmt = 'config.agents.skills.edited'

    def __init__(self, skill_id, tenant_uuid):
        content = {'id': int(skill_id)}
        super(SkillEditedEvent, self).__init__(content, tenant_uuid)
