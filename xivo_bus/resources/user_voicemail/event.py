# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

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
