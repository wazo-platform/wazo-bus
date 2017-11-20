# -*- coding: utf-8 -*-
# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditConferenceEvent(ResourceConfigEvent):
    name = 'conference_edited'
    routing_key = 'config.conferences.edited'


class CreateConferenceEvent(ResourceConfigEvent):
    name = 'conference_created'
    routing_key = 'config.conferences.created'


class DeleteConferenceEvent(ResourceConfigEvent):
    name = 'conference_deleted'
    routing_key = 'config.conferences.deleted'
