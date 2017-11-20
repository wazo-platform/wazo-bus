# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditVoicemailEvent(ResourceConfigEvent):
    name = 'voicemail_edited'
    routing_key = 'config.voicemail.edited'


class EditUserVoicemailEvent(object):
    name = 'user_voicemail_edited'

    def __init__(self, user_uuid, voicemail_id):
        self.user_uuid = user_uuid
        self.voicemail_id = int(voicemail_id)
        self.routing_key = 'config.users.{}.voicemails.edited'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)

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

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid and
                self.voicemail_id == other.voicemail_id)

    def __ne__(self, other):
        return not self == other


class CreateVoicemailEvent(ResourceConfigEvent):
    name = 'voicemail_created'
    routing_key = 'config.voicemail.created'


class DeleteVoicemailEvent(ResourceConfigEvent):
    name = 'voicemail_deleted'
    routing_key = 'config.voicemail.deleted'


class _UserVoicemailMessageEvent(object):

    def __init__(self, user_uuid, voicemail_id, message_id, message):
        self.user_uuid = user_uuid
        self.voicemail_id = voicemail_id
        self.message_id = message_id
        self.message = message
        self.required_acl = 'events.users.{}.voicemails'.format(self.user_uuid)

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'voicemail_id': self.voicemail_id,
            'message_id': self.message_id,
            'message': self.message,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['voicemail_id'],
            msg['message_id'],
            msg['message'])


class CreateUserVoicemailMessageEvent(_UserVoicemailMessageEvent):

    name = 'user_voicemail_message_created'
    routing_key = 'voicemails.messages.created'


class UpdateUserVoicemailMessageEvent(_UserVoicemailMessageEvent):

    name = 'user_voicemail_message_updated'
    routing_key = 'voicemails.messages.updated'


class DeleteUserVoicemailMessageEvent(_UserVoicemailMessageEvent):

    name = 'user_voicemail_message_deleted'
    routing_key = 'voicemails.messages.deleted'
