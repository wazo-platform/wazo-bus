# -*- coding: utf-8 -*-
# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseSipEndpointEvent(BaseEvent):

    def __init__(self, endpoint_sip):
        self._body = endpoint_sip
        super(_BaseSipEndpointEvent, self).__init__()


class EditSipEndpointEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_updated'
    routing_key_fmt = 'config.sip_endpoint.updated'


class CreateSipEndpointEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_created'
    routing_key_fmt = 'config.sip_endpoint.created'


class DeleteSipEndpointEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_deleted'
    routing_key_fmt = 'config.sip_endpoint.deleted'


class EditSipEndpointTemplateEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_template_updated'
    routing_key_fmt = 'config.sip_endpoint_template.updated'


class CreateSipEndpointTemplateEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_template_created'
    routing_key_fmt = 'config.sip_endpoint_template.created'


class DeleteSipEndpointTemplateEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_template_deleted'
    routing_key_fmt = 'config.sip_endpoint_template.deleted'
