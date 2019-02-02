# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import CollectdEvent


class ChannelCollectdEvent(CollectdEvent):
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
