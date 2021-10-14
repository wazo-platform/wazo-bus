# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseNetworkEvent(BaseEvent):
    def __init__(self, network):
        self._body = network
        super(_BaseNetworkEvent, self).__init__()


class CreateNetworkEvent(_BaseNetworkEvent):
    name = 'network_created'
    routing_key_fmt = 'config.networks.created'


class EditNetworkEvent(_BaseNetworkEvent):
    name = 'network_updated'
    routing_key_fmt = 'config.networks.updated'


class DeleteNetworkEvent(_BaseNetworkEvent):
    name = 'network_deleted'
    routing_key_fmt = 'config.networks.deleted'
