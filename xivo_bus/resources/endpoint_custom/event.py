# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseCustomEndpointEvent(BaseEvent):

    def __init__(self, endpoint_iax):
        self._body = endpoint_iax
        super(_BaseCustomEndpointEvent, self).__init__()


class EditCustomEndpointEvent(_BaseCustomEndpointEvent):
    name = 'custom_endpoint_updated'
    routing_key_fmt = 'config.custom_endpoint.updated'


class CreateCustomEndpointEvent(_BaseCustomEndpointEvent):
    name = 'custom_endpoint_created'
    routing_key_fmt = 'config.custom_endpoint.created'


class DeleteCustomEndpointEvent(_BaseCustomEndpointEvent):
    name = 'custom_endpoint_deleted'
    routing_key_fmt = 'config.custom_endpoint.deleted'
