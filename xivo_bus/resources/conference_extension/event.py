# -*- coding: utf-8 -*-

# Copyright (C) 2016 Francois Blackburn
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


class ConferenceExtensionConfigEvent(object):

    def __init__(self, conference_id, extension_id):
        self.conference_id = conference_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'conference_id': self.conference_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['conference_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.conference_id == other.conference_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class ConferenceExtensionAssociatedEvent(ConferenceExtensionConfigEvent):
    name = 'conference_extension_associated'
    routing_key = 'config.conferences.extensions.updated'


class ConferenceExtensionDissociatedEvent(ConferenceExtensionConfigEvent):
    name = 'conference_extension_dissociated'
    routing_key = 'config.conferences.extensions.deleted'
