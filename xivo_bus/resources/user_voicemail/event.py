# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserVoicemailConfigEvent(ResourceConfigEvent):

    def __init__(self, user_uuid, voicemail_id):
        self.user_uuid = user_uuid
        self._body = {
            'user_uuid': user_uuid,
            'voicemail_id': int(voicemail_id),
        }

    def marshal(self):
        return self._body

    def __ne__(self, other):
        return not self._body == other._body

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    @classmethod
    def unmarshal(cls, body):
        return cls(**body)


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
