# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserVoicemailConfigEvent(ResourceConfigEvent):

    def __init__(self, user_uuid, voicemail_id):
        self.user_uuid = user_uuid
        self.voicemail_id = int(voicemail_id)

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'voicemail_id': self.voicemail_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['voicemail_id'])


class UserVoicemailAssociatedEvent(UserVoicemailConfigEvent):
    name = 'voicemail_associated'

    def __init__(self, user_uuid, voicemail_id):
        super(UserVoicemailAssociatedEvent, self).__init__(user_uuid, voicemail_id)
        self.routing_key = 'config.users.{}.voicemails.updated'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)


class UserVoicemailDissociatedEvent(UserVoicemailConfigEvent):
    name = 'voicemail_dissociated'

    def __init__(self, user_uuid, voicemail_id):
        super(UserVoicemailDissociatedEvent, self).__init__(user_uuid, voicemail_id)
        self.routing_key = 'config.users.{}.voicemails.deleted'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)
