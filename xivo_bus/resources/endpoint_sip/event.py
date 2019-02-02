# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class SipEndpointConfigEvent(ResourceConfigEvent):
    pass


class EditSipEndpointEvent(SipEndpointConfigEvent):
    name = 'sip_endpoint_edited'
    routing_key = 'config.sip_endpoint.edited'


class CreateSipEndpointEvent(SipEndpointConfigEvent):
    name = 'sip_endpoint_created'
    routing_key = 'config.sip_endpoint.created'


class DeleteSipEndpointEvent(SipEndpointConfigEvent):
    name = 'sip_endpoint_deleted'
    routing_key = 'config.sip_endpoint.deleted'
