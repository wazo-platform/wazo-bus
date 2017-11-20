# -*- coding: utf-8 -*-
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditIvrEvent(ResourceConfigEvent):
    name = 'ivr_edited'
    routing_key = 'config.ivr.edited'


class CreateIvrEvent(ResourceConfigEvent):
    name = 'ivr_created'
    routing_key = 'config.ivr.created'


class DeleteIvrEvent(ResourceConfigEvent):
    name = 'ivr_deleted'
    routing_key = 'config.ivr.deleted'
