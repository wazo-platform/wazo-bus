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

from __future__ import unicode_literals

import string

from .common import CollectdEvent


def validate_plugin_instance_fragment(plugin_instance_fragment):
    result = ''.join(c for c in plugin_instance_fragment if (c in string.ascii_letters or
                                                             c in string.digits or
                                                             c == '-'))
    return result or '<unknown>'


class CallCollectdEvent(CollectdEvent):
    plugin = 'calls'
    plugin_instance = None
    routing_key = 'collectd.calls'
    type_ = 'counter'
    type_instance = None
    values = ('1',)

    def __init__(self, application, application_id, time=None):
        if time:
            self.time = int(time)

        application = validate_plugin_instance_fragment(application)
        application_id = validate_plugin_instance_fragment(application_id)

        self.plugin_instance = '{}.{}'.format(application, application_id)


class CallStartCollectdEvent(CallCollectdEvent):
    type_instance = 'start'


class CallConnectCollectdEvent(CallCollectdEvent):
    type_instance = 'connect'


class CallEndCollectdEvent(CallCollectdEvent):
    type_instance = 'end'


class CallAbandonedCollectdEvent(CallCollectdEvent):
    type_instance = 'abandoned'


class CallDurationCollectdEvent(CallCollectdEvent):
    type_ = 'gauge'
    type_instance = 'duration'

    def __init__(self, application, application_id, duration, time=None):
        super(CallDurationCollectdEvent, self).__init__(application, application_id, time)
        self.values = (str(round(duration, 3)),)
