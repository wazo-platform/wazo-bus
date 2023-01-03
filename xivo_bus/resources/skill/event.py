# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class SkillCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_created'
    routing_key_fmt = 'config.agents.skills.created'

    def __init__(self, skill_id, tenant_uuid):
        content = {'id': int(skill_id)}
        super().__init__(content, tenant_uuid)


class SkillDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_deleted'
    routing_key_fmt = 'config.agents.skills.deleted'

    def __init__(self, skill_id, tenant_uuid):
        content = {'id': int(skill_id)}
        super().__init__(content, tenant_uuid)


class SkillEditedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_edited'
    routing_key_fmt = 'config.agents.skills.edited'

    def __init__(self, skill_id, tenant_uuid):
        content = {'id': int(skill_id)}
        super().__init__(content, tenant_uuid)
