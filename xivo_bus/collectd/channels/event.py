# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from xivo_bus.collectd.common.event import CollectdEvent


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
