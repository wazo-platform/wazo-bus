# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditSkillEvent(ResourceConfigEvent):
    name = 'skill_edited'
    routing_key = 'config.agents.skills.edited'


class CreateSkillEvent(ResourceConfigEvent):
    name = 'skill_created'
    routing_key = 'config.agents.skills.created'


class DeleteSkillEvent(ResourceConfigEvent):
    name = 'skill_deleted'
    routing_key = 'config.agents.skills.deleted'
