# -*- coding: utf-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditPagingEvent(ResourceConfigEvent):
    name = 'paging_edited'
    routing_key = 'config.pagings.edited'


class CreatePagingEvent(ResourceConfigEvent):
    name = 'paging_created'
    routing_key = 'config.pagings.created'


class DeletePagingEvent(ResourceConfigEvent):
    name = 'paging_deleted'
    routing_key = 'config.pagings.deleted'
