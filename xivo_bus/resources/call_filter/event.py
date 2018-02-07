# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditCallFilterEvent(ResourceConfigEvent):
    name = 'call_filter_edited'
    routing_key = 'config.callfilter.edited'


class CreateCallFilterEvent(ResourceConfigEvent):
    name = 'call_filter_created'
    routing_key = 'config.callfilter.created'


class DeleteCallFilterEvent(ResourceConfigEvent):
    name = 'call_filter_deleted'
    routing_key = 'config.callfilter.deleted'


class EditCallFilterFallbackEvent(ResourceConfigEvent):
    name = 'call_filter_fallback_edited'
    routing_key = 'config.callfilters.fallbacks.edited'
