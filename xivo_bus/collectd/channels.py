# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import CollectdEvent


class _BaseChannelCollectdEvent(CollectdEvent):
    routing_key_fmt = 'collectd.channels'
    plugin = 'channels'
    plugin_instance = 'global'
    type_ = 'counter'
    type_instance = None
    values = ('1',)


class ChannelCreatedCollectdEvent(_BaseChannelCollectdEvent):
    name = 'collectd_channel_created'
    type_instance = 'created'


class ChannelEndedCollectdEvent(_BaseChannelCollectdEvent):
    name = 'collectd_channel_ended'
    type_instance = 'ended'
