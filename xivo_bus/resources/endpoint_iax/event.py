# -*- coding: utf-8 -*-
# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseIAXEndpointEvent(BaseEvent):

    def __init__(self, endpoint_iax):
        self._body = endpoint_iax
        super(_BaseIAXEndpointEvent, self).__init__()


class EditIAXEndpointEvent(_BaseIAXEndpointEvent):
    name = 'iax_endpoint_updated'
    routing_key_fmt = 'config.iax_endpoint.updated'


class CreateIAXEndpointEvent(_BaseIAXEndpointEvent):
    name = 'iax_endpoint_created'
    routing_key_fmt = 'config.iax_endpoint.created'


class DeleteIAXEndpointEvent(_BaseIAXEndpointEvent):
    name = 'iax_endpoint_deleted'
    routing_key_fmt = 'config.iax_endpoint.deleted'
