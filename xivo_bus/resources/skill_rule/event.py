# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditSkillRuleEvent(ResourceConfigEvent):
    name = 'skill_rule_edited'
    routing_key = 'config.queues.skillrules.edited'


class CreateSkillRuleEvent(ResourceConfigEvent):
    name = 'skill_rule_created'
    routing_key = 'config.queues.skillrules.created'


class DeleteSkillRuleEvent(ResourceConfigEvent):
    name = 'skill_rule_deleted'
    routing_key = 'config.queues.skillrules.deleted'
