# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class SkillRuleCreatedEvent(TenantEvent):
    name = 'skill_rule_created'
    routing_key_fmt = 'config.queues.skillrules.created'

    def __init__(self, skill_rule_id, tenant_uuid):
        content = {'id': int(skill_rule_id)}
        super(SkillRuleCreatedEvent, self).__init__(content, tenant_uuid)


class SkillRuleDeletedEvent(TenantEvent):
    name = 'skill_rule_deleted'
    routing_key_fmt = 'config.queues.skillrules.deleted'

    def __init__(self, skill_rule_id, tenant_uuid):
        content = {'id': int(skill_rule_id)}
        super(SkillRuleDeletedEvent, self).__init__(content, tenant_uuid)


class SkillRuleEditedEvent(TenantEvent):
    name = 'skill_rule_edited'
    routing_key_fmt = 'config.queues.skillrules.edited'

    def __init__(self, skill_rule_id, tenant_uuid):
        content = {'id': int(skill_rule_id)}
        super(SkillRuleEditedEvent, self).__init__(content, tenant_uuid)
