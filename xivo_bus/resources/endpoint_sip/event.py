# -*- coding: utf-8 -*-
# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseSipEndpointEvent(BaseEvent):

    def __init__(self, endpoint_sip):
        self._body = endpoint_sip
        super(_BaseSipEndpointEvent, self).__init__()

    def __eq__(self, other):
        if self is other:
            return True

        return self.__class__ == other.__class__ and self._body == other._body

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self._body)

    def __repr__(self):
        return self.__str__()


class EditSipEndpointEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_updated'
    routing_key_fmt = 'config.sip_endpoint.updated'


class CreateSipEndpointEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_created'
    routing_key_fmt = 'config.sip_endpoint.created'


class DeleteSipEndpointEvent(_BaseSipEndpointEvent):
    name = 'sip_endpoint_deleted'
    routing_key_fmt = 'config.sip_endpoint.deleted'
