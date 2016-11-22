# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
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


class OutcallExtensionConfigEvent(object):

    def __init__(self, outcall_id, extension_id):
        self.outcall_id = outcall_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'outcall_id': self.outcall_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['outcall_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.outcall_id == other.outcall_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class OutcallExtensionAssociatedEvent(OutcallExtensionConfigEvent):
    name = 'outcall_extension_associated'
    routing_key = 'config.outcalls.extensions.updated'


class OutcallExtensionDissociatedEvent(OutcallExtensionConfigEvent):
    name = 'outcall_extension_dissociated'
    routing_key = 'config.outcalls.extensions.deleted'
