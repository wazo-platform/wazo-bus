# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import AbstractCollectdEvent


class ChannelCollectdEvent(AbstractCollectdEvent):
    plugin = 'channels'
    plugin_instance = 'global'
    routing_key = 'collectd.channels'
    type_ = 'counter'
    type_instance = None
    values = ('1',)


class ChannelCreatedCollectdEvent(ChannelCollectdEvent):
    type_instance = 'created'


class ChannelEndedCollectdEvent(ChannelCollectdEvent):
    type_instance = 'ended'
