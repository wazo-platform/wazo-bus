# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class SccpEndpointConfigEvent(ResourceConfigEvent):
    pass


class EditSccpEndpointEvent(SccpEndpointConfigEvent):
    name = 'sccp_endpoint_edited'
    routing_key = 'config.sccp_endpoint.edited'


class CreateSccpEndpointEvent(SccpEndpointConfigEvent):
    name = 'sccp_endpoint_created'
    routing_key = 'config.sccp_endpoint.created'


class DeleteSccpEndpointEvent(SccpEndpointConfigEvent):
    name = 'sccp_endpoint_deleted'
    routing_key = 'config.sccp_endpoint.deleted'
