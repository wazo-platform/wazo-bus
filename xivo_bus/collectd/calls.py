# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import string

from .common import CollectdEvent


def validate_plugin_instance_fragment(plugin_instance_fragment):
    result = ''.join(c for c in plugin_instance_fragment if (c in string.ascii_letters
                                                             or c in string.digits
                                                             or c == '-'))
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
        if application_id is not None:
            application_id = validate_plugin_instance_fragment(application_id)
            self.plugin_instance = '{}.{}'.format(application, application_id)
        else:
            self.plugin_instance = application


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
