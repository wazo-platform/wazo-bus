# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent


class VoicemailCreatedEvent(TenantEvent):
    name = 'voicemail_created'
    routing_key_fmt = 'config.voicemail.created'

    def __init__(self, voicemail_id, tenant_uuid):
        content = {'id': int(voicemail_id)}
        super(VoicemailCreatedEvent, self).__init__(content, tenant_uuid)


class VoicemailDeletedEvent(TenantEvent):
    name = 'voicemail_deleted'
    routing_key_fmt = 'config.voicemail.deleted'

    def __init__(self, voicemail_id, tenant_uuid):
        content = {'id': int(voicemail_id)}
        super(VoicemailDeletedEvent, self).__init__(content, tenant_uuid)


class VoicemailEditedEvent(TenantEvent):
    name = 'voicemail_edited'
    routing_key_fmt = 'config.voicemail.edited'

    def __init__(self, voicemail_id, tenant_uuid):
        content = {'id': int(voicemail_id)}
        super(VoicemailEditedEvent, self).__init__(content, tenant_uuid)


class UserVoicemailEditedEvent(UserEvent):
    name = 'user_voicemail_edited'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.edited'

    def __init__(self, voicemail_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
        }
        super(UserVoicemailEditedEvent, self).__init__(content, tenant_uuid, user_uuid)


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
            msg['user_uuid'], msg['voicemail_id'], msg['message_id'], msg['message']
        )


class CreateUserVoicemailMessageEvent(_UserVoicemailMessageEvent):

    name = 'user_voicemail_message_created'
    routing_key = 'voicemails.messages.created'


class UpdateUserVoicemailMessageEvent(_UserVoicemailMessageEvent):

    name = 'user_voicemail_message_updated'
    routing_key = 'voicemails.messages.updated'


class DeleteUserVoicemailMessageEvent(_UserVoicemailMessageEvent):

    name = 'user_voicemail_message_deleted'
    routing_key = 'voicemails.messages.deleted'
