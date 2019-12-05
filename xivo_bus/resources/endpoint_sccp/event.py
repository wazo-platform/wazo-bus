# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseSccpEndpointEvent(BaseEvent):

    def __init__(self, endpoint_iax):
        self._body = endpoint_iax
        super(_BaseSccpEndpointEvent, self).__init__()


class EditSccpEndpointEvent(_BaseSccpEndpointEvent):
    name = 'sccp_endpoint_updated'
    routing_key_fmt = 'config.sccp_endpoint.updated'


class CreateSccpEndpointEvent(_BaseSccpEndpointEvent):
    name = 'sccp_endpoint_created'
    routing_key_fmt = 'config.sccp_endpoint.created'


class DeleteSccpEndpointEvent(_BaseSccpEndpointEvent):
    name = 'sccp_endpoint_deleted'
    routing_key_fmt = 'config.sccp_endpoint.deleted'
