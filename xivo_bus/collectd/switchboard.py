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

from .common import CollectdEvent


class _SwitchboardCollectdEvent(CollectdEvent):

    plugin = 'switchboard'
    plugin_instance = None
    routing_key = 'collectd.switchboard'
    type_ = 'counter'
    type_instance = None
    values = ('1',)

    def __init__(self, switchboard_name, time=None):
        if time:
            self.time = int(time)

        self.plugin_instance = 'switchboard.{}'.format(switchboard_name)


class SwitchboardEnteredEvent(_SwitchboardCollectdEvent):
    type_instance = 'entered'


class SwitchboardCompletedEvent(_SwitchboardCollectdEvent):
    type_instance = 'completed'


class SwitchboardAbandonedEvent(_SwitchboardCollectdEvent):
    type_instance = 'abandoned'


class SwitchboardForwardedEvent(_SwitchboardCollectdEvent):
    type_instance = 'forwarded'


class SwitchboardTransferedEvent(_SwitchboardCollectdEvent):
    type_instance = 'transfered'


class SwitchboardWaitTimeEvent(_SwitchboardCollectdEvent):
    type_instance = 'wait'
    type_ = 'gauge'

    def __init__(self, switchboard_name, duration, time=None):
        super(SwitchboardWaitTimeEvent, self).__init__(switchboard_name, time)
        self.values = (str(round(duration, 3)),)
