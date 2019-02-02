# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditIAXEndpointEvent(ResourceConfigEvent):
    name = 'iax_endpoint_edited'
    routing_key = 'config.iax_endpoint.edited'


class CreateIAXEndpointEvent(ResourceConfigEvent):
    name = 'iax_endpoint_created'
    routing_key = 'config.iax_endpoint.created'


class DeleteIAXEndpointEvent(ResourceConfigEvent):
    name = 'iax_endpoint_deleted'
    routing_key = 'config.iax_endpoint.deleted'
